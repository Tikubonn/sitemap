
import pytest
import shutil
import datetime
from pathlib import Path
from sitemap.image_sitemap import ImageSitemapFile, Image
from collections import OrderedDict

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_image_sitemap_file ():
  image_sitemap_file = ImageSitemapFile(TEST_DIR.joinpath("sample.xml"), OrderedDict([
    ("http://www.example.com/page.html", [
      Image("http://www.example.com/top-image.png"),
      Image("http://www.example.com/top-image2.png", caption="caption"),
      Image("http://www.example.com/top-image3.png", caption="caption", geo_location="geo location"),
      Image("http://www.example.com/top-image4.png", caption="caption", geo_location="geo location", title="title"),
      Image("http://www.example.com/top-image5.png", caption="caption", geo_location="geo location", title="title", license="license"),
    ])
  ]))
  image_sitemap_file.save()
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\"><url><loc>http://www.example.com/page.html</loc><image:image><image:loc>http://www.example.com/top-image.png</image:loc></image:image><image:image><image:loc>http://www.example.com/top-image2.png</image:loc><image:caption>caption</image:caption></image:image><image:image><image:loc>http://www.example.com/top-image3.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location></image:image><image:image><image:loc>http://www.example.com/top-image4.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location><image:title>title</image:title></image:image><image:image><image:loc>http://www.example.com/top-image5.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location><image:title>title</image:title><image:license>license</image:license></image:image></url></urlset>"

def test_image_sitemap_file_with_indent ():
  image_sitemap_file = ImageSitemapFile(TEST_DIR.joinpath("sample.xml"), OrderedDict([
    ("http://www.example.com/page.html", [
      Image("http://www.example.com/top-image.png"),
      Image("http://www.example.com/top-image2.png", caption="caption"),
      Image("http://www.example.com/top-image3.png", caption="caption", geo_location="geo location"),
      Image("http://www.example.com/top-image4.png", caption="caption", geo_location="geo location", title="title"),
      Image("http://www.example.com/top-image5.png", caption="caption", geo_location="geo location", title="title", license="license"),
    ])
  ]))
  image_sitemap_file.save(use_indent=True)
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <image:image>
      <image:loc>http://www.example.com/top-image.png</image:loc>
    </image:image>
    <image:image>
      <image:loc>http://www.example.com/top-image2.png</image:loc>
      <image:caption>caption</image:caption>
    </image:image>
    <image:image>
      <image:loc>http://www.example.com/top-image3.png</image:loc>
      <image:caption>caption</image:caption>
      <image:geo_location>geo location</image:geo_location>
    </image:image>
    <image:image>
      <image:loc>http://www.example.com/top-image4.png</image:loc>
      <image:caption>caption</image:caption>
      <image:geo_location>geo location</image:geo_location>
      <image:title>title</image:title>
    </image:image>
    <image:image>
      <image:loc>http://www.example.com/top-image5.png</image:loc>
      <image:caption>caption</image:caption>
      <image:geo_location>geo location</image:geo_location>
      <image:title>title</image:title>
      <image:license>license</image:license>
    </image:image>
  </url>
</urlset>"""
