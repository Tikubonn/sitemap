
import pytest
import shutil
import datetime
from pathlib import Path
# from sitemap import SitemapIndexFile
from sitemap.sitemap_index import SitemapIndexFile

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_sitemap_index_file ():
  sitemap_index_file = SitemapIndexFile(TEST_DIR.joinpath("sample.xml"), [
    ("http://www.example.com/sitemap.xml", datetime.datetime(2025, 1, 23)),
    ("http://www.example.com/sitemap2.xml", datetime.datetime(2025, 1, 23)),
    ("http://www.example.com/sitemap3.xml", datetime.datetime(2025, 1, 23)),
  ])
  sitemap_index_file.save()
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><sitemap><loc>http://www.example.com/sitemap.xml</loc><lastmod>2025-01-23</lastmod></sitemap><sitemap><loc>http://www.example.com/sitemap2.xml</loc><lastmod>2025-01-23</lastmod></sitemap><sitemap><loc>http://www.example.com/sitemap3.xml</loc><lastmod>2025-01-23</lastmod></sitemap></sitemapindex>"

def test_sitemap_index_file_with_indent ():
  sitemap_index_file = SitemapIndexFile(TEST_DIR.joinpath("sample.xml"), [
    ("http://www.example.com/sitemap.xml", datetime.datetime(2025, 1, 23)),
    ("http://www.example.com/sitemap2.xml", datetime.datetime(2025, 1, 23)),
    ("http://www.example.com/sitemap3.xml", datetime.datetime(2025, 1, 23)),
  ])
  sitemap_index_file.save(use_indent=True)
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
