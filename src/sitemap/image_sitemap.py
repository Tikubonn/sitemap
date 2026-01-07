
import sqlite3
import importlib.resources
import itertools
from io import TextIOBase, StringIO
from xml.etree import ElementTree as ETree
from typing import NamedTuple, ClassVar
from pathlib import Path
from closeable import ICloseable, Closeable
from xmlschema import XMLSchema
from collections import OrderedDict
from .abc import ISitemap, ISitemapFile, ILoadable

class Image (NamedTuple):

  loc:str
  caption:str = ""
  geo_location:str = ""
  title:str = ""
  license:str = ""

class URL (NamedTuple):

  loc:str
  images:list[Image]

class ImageSitemapFile (ISitemapFile):

  def __init__ (self, file:Path|str, url_images:OrderedDict[str, list[Image]]):
    self._file = Path(file)
    self._url_images = url_images

  @property
  def file (self) -> Path:
    return self._file

  def _as_element (self) -> ETree.Element:
    urlset_node = ETree.Element("urlset", {
      "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1",
    })
    for loc, images in self._url_images.items():
      url_node = ETree.SubElement(urlset_node, "url")
      loc_node = ETree.SubElement(url_node, "loc")
      loc_node.text = loc
      for image_loc, image_caption, image_geo_location, image_title, image_license in images:
        image_node = ETree.SubElement(url_node, "image:image")
        image_loc_node = ETree.SubElement(image_node, "image:loc") 
        image_loc_node.text = image_loc
        if image_caption:
          image_caption_node = ETree.SubElement(image_node, "image:caption") 
          image_caption_node.text = image_caption
        if image_geo_location:
          image_geo_location_node = ETree.SubElement(image_node, "image:geo_location") 
          image_geo_location_node.text = image_geo_location
        if image_title:
          image_title_node = ETree.SubElement(image_node, "image:title") 
          image_title_node.text = image_title
        if image_license:
          image_license_node = ETree.SubElement(image_node, "image:license")
          image_license_node.text = image_license
    return urlset_node

  def save (self, use_indent:bool=False):
    element = self._as_element()
    if use_indent:
      ETree.indent(element)
    with open(self._file, "wb") as file:
      for part in ETree.tostringlist(element, encoding="utf-8", xml_declaration=True):
        file.write(part)

class ImageSitemap (ISitemap, ILoadable, ICloseable):

  def _db_prepare (self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE image(id INTEGER PRIMARY KEY AUTOINCREMENT, loc TEXT, image_loc TEXT, image_caption TEXT, image_geo_location TEXT, image_title TEXT, image_license TEXT)")
    return connection, cursor

  def __init__ (self, file:Path|str):
    self._file = Path(file)
    self._connection, self._cursor = self._db_prepare()
    self._closeable = Closeable(self._close_handler)

  def __enter__ (self):
    return self

  def __exit__ (self, exc_type, exc_value, traceback):
    self._closeable.close()

  @property
  def closed (self) -> bool:
    return self._closeable.closed

  def _close_handler (self):
    self._cursor.close()
    self._connection.close()

  def close (self):
    self._closeable.close()

  def register (self, loc:str, image_loc:str, image_caption:str="", image_geo_location:str="", image_title:str="", image_license:str=""):
    self._closeable.must_be_open()
    self._cursor.execute("SELECT id FROM image WHERE loc == ? AND image_loc == ?", (loc, image_loc))
    if self._cursor.fetchone():
      self._cursor.execute("UPDATE image SET image_caption = ?, image_geo_location = ?, image_title = ?, image_license = ? WHERE loc == ? AND image_loc == ?", (image_caption, image_geo_location, image_title, image_license, loc, image_loc))
    else:
      self._cursor.execute("INSERT INTO image(loc, image_loc, image_caption, image_geo_location, image_title, image_license) VALUES(?, ?, ?, ?, ?, ?)", (loc, image_loc, image_caption, image_geo_location, image_title, image_license))

  def unregister (self, loc:str, image_loc:str):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM image WHERE loc == ? AND image_loc == ?", (loc, image_loc))

  def clear (self):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM image")

  def get (self, loc:str) -> URL|None:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT image_loc, image_caption, image_geo_location, image_title, image_license FROM image WHERE loc == ? ORDER BY image_loc ASC", (loc,))
    found_columns = self._cursor.fetchall()
    if found_columns:
      images = [Image(image_loc, image_caption, image_geo_location, image_title, image_license) for image_loc, image_caption, image_geo_location, image_title, image_license in found_columns]
      return URL(loc, images)
    else:
      return None

  def list_all (self) -> list[URL]:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT loc, image_loc, image_caption, image_geo_location, image_title, image_license FROM image ORDER BY loc ASC, image_loc ASC")
    url_images = OrderedDict()
    result = []
    for loc, image_loc, image_caption, image_geo_location, image_title, image_license in self._cursor.fetchall():
      url_images.setdefault(loc, [])
      url_images[loc].append(Image(image_loc, image_caption, image_geo_location, image_title, image_license))
    for loc, images in url_images.items():
      result.append(URL(loc, images))
    return result

  def save_files (self, use_indent:bool=False) -> list[ISitemapFile]:
    self._cursor.execute("SELECT loc, image_loc, image_caption, image_geo_location, image_title, image_license FROM image ORDER BY loc ASC, image_loc ASC")
    url_images = OrderedDict()
    for loc, image_loc, image_caption, image_geo_location, image_title, image_license in self._cursor.fetchall():
      url_images.setdefault(loc, [])
      url_images[loc].append(Image(image_loc, image_caption, image_geo_location, image_title, image_license))
    result = []
    for index, batched_url_images in enumerate(itertools.batched(url_images.items(), 50000)):
      if 0 < index:
        save_file = self._file.with_stem("{:s}{:d}".format(self._file.stem, index +1))
      else:
        save_file = self._file
      image_sitemap_file = ImageSitemapFile(save_file, OrderedDict(batched_url_images))
      image_sitemap_file.save(use_indent=use_indent)
      result.append(image_sitemap_file)
    return result

  _XML_SCHEMA_TO_PARSE:ClassVar[XMLSchema] = XMLSchema(importlib.resources.files("sitemap").joinpath("static/xsd/sitemap.xsd"), build=False)
  _XML_SCHEMA_TO_PARSE.add_schema(importlib.resources.files("sitemap").joinpath("static/xsd/sitemap-image.xsd"))
  _XML_SCHEMA_TO_PARSE.build()

  def load (self, stream:TextIOBase):
    self._closeable.must_be_open()
    root = self._XML_SCHEMA_TO_PARSE.to_dict(stream)
    for url in root["url"]:
      loc_source = url["loc"]
      if loc_source:
        loc = loc_source
      else:
        raise ValueError()
      images = url["image:image"]
      if images:
        for image in images:
          image_loc_source = image["image:loc"]
          if image_loc_source:
            image_loc = image_loc_source
          else:
            raise ValueError()
          image_caption_source = image.get("image:caption")
          if image_caption_source:
            image_caption = image_caption_source
          else:
            image_caption = ""
          image_geo_location_source = image.get("image:geo_location")
          if image_geo_location_source:
            image_geo_location = image_geo_location_source
          else:
            image_geo_location = ""
          image_title_source = image.get("image:title")
          if image_title_source:
            image_title = image_title_source
          else:
            image_title = ""
          image_license_source = image.get("image:license")
          if image_license_source:
            image_license = image_license_source
          else:
            image_license = ""
          self.register(loc, image_loc, image_caption, image_geo_location, image_title, image_license)
      else:
        raise ValueError()

  def loads (self, source:str):
    with StringIO(source) as stream:
      self.load(stream)
