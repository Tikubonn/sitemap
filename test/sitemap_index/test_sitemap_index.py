
import pytest
import shutil
import datetime
from io import StringIO
from pathlib import Path
from sitemap.sitemap_index import SitemapIndex, Sitemap

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_sitemap_index ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert [sitemap_file.file for sitemap_file in sitemap_index.save_files()] == [TEST_DIR.joinpath("sample.xml")]
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><sitemap><loc>http://www.example.com/sitemap.xml</loc><lastmod>2025-01-23</lastmod></sitemap><sitemap><loc>http://www.example.com/sitemap2.xml</loc><lastmod>2025-01-23</lastmod></sitemap><sitemap><loc>http://www.example.com/sitemap3.xml</loc><lastmod>2025-01-23</lastmod></sitemap></sitemapindex>"

def test_sitemap_index2 ():

  #未登録の SitemapIndex はファイルを作成しない。

  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  assert [sitemap_file.file for sitemap_file in sitemap_index.save_files()] == []

def test_sitemap_index_with_indent ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert [sitemap_file.file for sitemap_file in sitemap_index.save_files(use_indent=True)] == [TEST_DIR.joinpath("sample.xml")]
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap2.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap3.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
</sitemapindex>"""

def test_sitemap_index_get ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap_index.get("http://www.example.com/sitemap.xml") == Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap_index.get("http://www.example.com/sitemap2.xml") == Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap_index.get("http://www.example.com/sitemap3.xml") == Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap_index.get("http://www.example.com/not-found.xml") is None

def test_sitemap_index_clear ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap.xml") == Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap2.xml") == Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap3.xml") == Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.clear()
  assert sitemap_index.get("http://www.example.com/sitemap.xml") is None
  assert sitemap_index.get("http://www.example.com/sitemap2.xml") is None
  assert sitemap_index.get("http://www.example.com/sitemap3.xml") is None

def test_sitemap_index_unregister ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap.xml") == Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap2.xml") == Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap3.xml") == Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.unregister("http://www.example.com/sitemap.xml")
  sitemap_index.unregister("http://www.example.com/sitemap2.xml")
  sitemap_index.unregister("http://www.example.com/sitemap3.xml")
  assert sitemap_index.get("http://www.example.com/sitemap.xml") is None
  assert sitemap_index.get("http://www.example.com/sitemap2.xml") is None
  assert sitemap_index.get("http://www.example.com/sitemap3.xml") is None

def test_sitemap_index_unregister2 ():

  #未登録のデータを抹消した場合の動作確認

  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap.xml") == Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap2.xml") == Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap3.xml") == Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.unregister("http://www.example.com/not-found.xml")
  sitemap_index.get("http://www.example.com/sitemap.xml") == Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap2.xml") == Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.get("http://www.example.com/sitemap3.xml") == Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))

def test_sitemap_index_list_all ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
  sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap_index.list_all() == [
    Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23)),
  ]

def test_sitemap_index_load ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  with StringIO("""<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap2.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap3.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
</sitemapindex>
""") as file:
    sitemap_index.load(file)
  assert sitemap_index.list_all() == [
    Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23)),
  ]

def test_sitemap_index_loads ():
  sitemap_index = SitemapIndex(TEST_DIR.joinpath("sample.xml"))
  sitemap_index.loads("""<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap2.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap3.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
</sitemapindex>
""")
  assert sitemap_index.list_all() == [
    Sitemap("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23)),
    Sitemap("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23)),
  ]
