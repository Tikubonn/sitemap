
import pytest
import shutil
import datetime
from io import StringIO
from pathlib import Path
from sitemap.image_sitemap import ImageSitemap, Image, URL
from collections import OrderedDict

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_image_sitemap ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png", image_caption="caption")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png", image_caption="caption", image_geo_location="geo location")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image4.png", image_caption="caption", image_geo_location="geo location", image_title="title")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image5.png", image_caption="caption", image_geo_location="geo location", image_title="title", image_license="license")
  assert [sitemap_file.file for sitemap_file in image_sitemap.save_files()] == [TEST_DIR.joinpath("sample.xml")]
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\"><url><loc>http://www.example.com/page.html</loc><image:image><image:loc>http://www.example.com/top-image.png</image:loc></image:image><image:image><image:loc>http://www.example.com/top-image2.png</image:loc><image:caption>caption</image:caption></image:image><image:image><image:loc>http://www.example.com/top-image3.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location></image:image><image:image><image:loc>http://www.example.com/top-image4.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location><image:title>title</image:title></image:image><image:image><image:loc>http://www.example.com/top-image5.png</image:loc><image:caption>caption</image:caption><image:geo_location>geo location</image:geo_location><image:title>title</image:title><image:license>license</image:license></image:image></url></urlset>"

def test_image_sitemap2 ():

  #未登録の ImageSitemap はファイルを作成しない。

  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  assert [sitemap_file.file for sitemap_file in image_sitemap.save_files()] == []

def test_image_sitemap_with_indent ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png", image_caption="caption")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png", image_caption="caption", image_geo_location="geo location")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image4.png", image_caption="caption", image_geo_location="geo location", image_title="title")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image5.png", image_caption="caption", image_geo_location="geo location", image_title="title", image_license="license")
  assert [sitemap_file.file for sitemap_file in image_sitemap.save_files(use_indent=True)] == [TEST_DIR.joinpath("sample.xml")]
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

def test_image_sitemap_get ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png", image_caption="caption")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png", image_caption="caption", image_geo_location="geo location")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image4.png", image_caption="caption", image_geo_location="geo location", image_title="title")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image5.png", image_caption="caption", image_geo_location="geo location", image_title="title", image_license="license")
  assert image_sitemap.get("http://www.example.com/page.html") == URL(
    loc="http://www.example.com/page.html",
    images=[
      Image("http://www.example.com/top-image.png"),
      Image("http://www.example.com/top-image2.png", caption="caption"),
      Image("http://www.example.com/top-image3.png", caption="caption", geo_location="geo location"),
      Image("http://www.example.com/top-image4.png", caption="caption", geo_location="geo location", title="title"),
      Image("http://www.example.com/top-image5.png", caption="caption", geo_location="geo location", title="title", license="license"),
    ]
  )
  assert image_sitemap.get("http://www.example.com/not-found.html") is None

def test_image_sitemap_clear ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png")
  image_sitemap.clear()
  assert image_sitemap.get("http://www.example.com/page.html") is None
  assert image_sitemap.get("http://www.example.com/not-found.html") is None

def test_image_sitemap_unregister ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png")
  assert image_sitemap.get("http://www.example.com/page.html") == URL(
    loc="http://www.example.com/page.html",
    images=[
      Image("http://www.example.com/top-image.png"),
      Image("http://www.example.com/top-image2.png"),
      Image("http://www.example.com/top-image3.png"),
    ]
  )
  image_sitemap.unregister("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  assert image_sitemap.get("http://www.example.com/page.html") == URL(
    loc="http://www.example.com/page.html",
    images=[
      Image("http://www.example.com/top-image2.png"),
      Image("http://www.example.com/top-image3.png"),
    ]
  )
  image_sitemap.unregister("http://www.example.com/page.html", "http://www.example.com/top-image2.png")
  assert image_sitemap.get("http://www.example.com/page.html") == URL(
    loc="http://www.example.com/page.html",
    images=[
      Image("http://www.example.com/top-image3.png"),
    ]
  )
  image_sitemap.unregister("http://www.example.com/page.html", "http://www.example.com/top-image3.png")
  assert image_sitemap.get("http://www.example.com/page.html") is None

def test_image_sitemap_unregister2 ():

  #未登録のデータを抹消した場合の動作確認

  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png")
  image_sitemap.unregister("http://www.example.com/page.html", "http://www.example.com/not-found.png")
  image_sitemap.unregister("http://www.example.com/not-found.html", "http://www.example.com/top-image.png")
  assert image_sitemap.get("http://www.example.com/page.html") == URL(
    loc="http://www.example.com/page.html",
    images=[
      Image("http://www.example.com/top-image.png"),
      Image("http://www.example.com/top-image2.png"),
      Image("http://www.example.com/top-image3.png"),
    ]
  )

def test_image_sitemap_list_all ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png")
  image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image3.png")
  assert image_sitemap.list_all() == [
    URL(
      loc="http://www.example.com/page.html",
      images=[
        Image("http://www.example.com/top-image.png"),
        Image("http://www.example.com/top-image2.png"),
        Image("http://www.example.com/top-image3.png"),
      ]
    )
  ]

def test_image_sitemap_load ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  with StringIO("""<?xml version='1.0' encoding='utf-8'?>
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
</urlset>
""") as file:
    image_sitemap.load(file)
  assert image_sitemap.list_all() == [
    URL(
      loc="http://www.example.com/page.html",
      images=[
        Image(
          loc="http://www.example.com/top-image.png"
        ),
        Image(
          loc="http://www.example.com/top-image2.png",
          caption="caption"
        ),
        Image(
          loc="http://www.example.com/top-image3.png",
          caption="caption",
          geo_location="geo location"
        ),
        Image(
          loc="http://www.example.com/top-image4.png",
          caption="caption",
          geo_location="geo location",
          title="title"
        ),
        Image(
          loc="http://www.example.com/top-image5.png",
          caption="caption",
          geo_location="geo location",
          title="title",
          license="license"
        )
      ]
    )
  ]

def test_image_sitemap_loads ():
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("sample.xml"))
  image_sitemap.loads("""<?xml version='1.0' encoding='utf-8'?>
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
</urlset>
""")
  assert image_sitemap.list_all() == [
    URL(
      loc="http://www.example.com/page.html",
      images=[
        Image(
          loc="http://www.example.com/top-image.png"
        ),
        Image(
          loc="http://www.example.com/top-image2.png",
          caption="caption"
        ),
        Image(
          loc="http://www.example.com/top-image3.png",
          caption="caption",
          geo_location="geo location"
        ),
        Image(
          loc="http://www.example.com/top-image4.png",
          caption="caption",
          geo_location="geo location",
          title="title"
        ),
        Image(
          loc="http://www.example.com/top-image5.png",
          caption="caption",
          geo_location="geo location",
          title="title",
          license="license"
        )
      ]
    )
  ]
