
import pytest
import shutil
import datetime
from pathlib import Path
from sitemap import Sitemap, ImageSitemap, SitemapIndex, Host, AutoSitemapIndex

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_auto_sitemap_index ():
  host = Host("http", "www.example.com", TEST_DIR)
  sitemap = Sitemap(TEST_DIR.joinpath("sitemap.xml"))
  sitemap.register("http://www.example.com/", last_mod=datetime.datetime(2025, 1, 23))
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("image-sitemap.xml"))
  image_sitemap.register("http://www.example.com/", image_loc="http://www.example.com/top-image.png")
  auto_sitemap_index = AutoSitemapIndex(host, TEST_DIR.joinpath("sitemap-index.xml"), [sitemap, image_sitemap])
  assert [sitemap_file.file for sitemap_file in auto_sitemap_index.save_files()] == [
    TEST_DIR.joinpath("sitemap.xml"),
    TEST_DIR.joinpath("image-sitemap.xml"),
    TEST_DIR.joinpath("sitemap-index.xml"),
  ]
  with open(TEST_DIR.joinpath("sitemap.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://www.example.com/</loc><lastmod>2025-01-23</lastmod></url></urlset>"
  with open(TEST_DIR.joinpath("image-sitemap.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\"><url><loc>http://www.example.com/</loc><image:image><image:loc>http://www.example.com/top-image.png</image:loc></image:image></url></urlset>"
  with open(TEST_DIR.joinpath("sitemap-index.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><sitemap><loc>http://www.example.com/image-sitemap.xml</loc><lastmod>{today:s}</lastmod></sitemap><sitemap><loc>http://www.example.com/sitemap.xml</loc><lastmod>{today:s}</lastmod></sitemap></sitemapindex>".format(today=datetime.date.today().isoformat())

def test_auto_sitemap_index2 ():

  #未登録の AutoSitemapIndex はファイルを作成しない。

  host = Host("http", "www.example.com", TEST_DIR)
  sitemap = Sitemap(TEST_DIR.joinpath("sitemap.xml"))
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("image-sitemap.xml"))
  auto_sitemap_index = AutoSitemapIndex(host, TEST_DIR.joinpath("sitemap-index.xml"), [sitemap, image_sitemap])
  assert [sitemap_file.file for sitemap_file in auto_sitemap_index.save_files()] == []

def test_auto_sitemap_index_with_indent ():
  host = Host("http", "www.example.com", TEST_DIR)
  sitemap = Sitemap(TEST_DIR.joinpath("sitemap.xml"))
  sitemap.register("http://www.example.com/", last_mod=datetime.datetime(2025, 1, 23))
  image_sitemap = ImageSitemap(TEST_DIR.joinpath("image-sitemap.xml"))
  image_sitemap.register("http://www.example.com/", image_loc="http://www.example.com/top-image.png")
  auto_sitemap_index = AutoSitemapIndex(host, TEST_DIR.joinpath("sitemap-index.xml"), [sitemap, image_sitemap])
  assert [sitemap_file.file for sitemap_file in auto_sitemap_index.save_files(use_indent=True)] == [
    TEST_DIR.joinpath("sitemap.xml"),
    TEST_DIR.joinpath("image-sitemap.xml"),
    TEST_DIR.joinpath("sitemap-index.xml"),
  ]
  with open(TEST_DIR.joinpath("sitemap.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
</urlset>"""
  with open(TEST_DIR.joinpath("image-sitemap.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\">
  <url>
    <loc>http://www.example.com/</loc>
    <image:image>
      <image:loc>http://www.example.com/top-image.png</image:loc>
    </image:image>
  </url>
</urlset>"""
  with open(TEST_DIR.joinpath("sitemap-index.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <sitemap>
    <loc>http://www.example.com/image-sitemap.xml</loc>
    <lastmod>{today:s}</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>{today:s}</lastmod>
  </sitemap>
</sitemapindex>""".format(today=datetime.date.today().isoformat())

def test_auto_sitemap_index3 ():

  #sitemap_indexes 属性を指定した場合の動作確認です。

  host = Host("http", "www.example.com", TEST_DIR)
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("inner-sitemap-index.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  auto_sitemap_index = AutoSitemapIndex(host, TEST_DIR.joinpath("sitemap-index.xml"), [], sitemap_indexes=[sitemap_index])
  assert [sitemap_file.file for sitemap_file in auto_sitemap_index.save_files(use_indent=True)] == [
    TEST_DIR.joinpath("sitemap-index.xml")
  ]
  assert TEST_DIR.joinpath("inner-sitemap-index.xml").exists() == False
  assert TEST_DIR.joinpath("sitemap-index.xml").exists() == True
  with open(TEST_DIR.joinpath("sitemap-index.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap2.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
</sitemapindex>"""
