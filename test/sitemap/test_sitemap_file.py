
import pytest
import shutil
import datetime
from pathlib import Path
from sitemap.sitemap import ChangeFreq, SitemapFile

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_sitemap_file ():
  sitemap_file = SitemapFile(TEST_DIR.joinpath("sample.xml"), [
    ("http://www.example.com/page.html", datetime.datetime(2025, 1, 23), 0.5, ChangeFreq.NONE),
    ("http://www.example.com/page2.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.NONE),
    ("http://www.example.com/page3.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.HOURLY),
    ("http://www.example.com/page4.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.DAILY),
    ("http://www.example.com/page5.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.WEEKLY),
    ("http://www.example.com/page6.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.MONTHLY),
    ("http://www.example.com/page7.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.YEARLY),
    ("http://www.example.com/page8.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.ALWAYS),
    ("http://www.example.com/page9.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.NEVER),
  ])
  sitemap_file.save()
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://www.example.com/page.html</loc><lastmod>2025-01-23</lastmod></url><url><loc>http://www.example.com/page2.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority></url><url><loc>http://www.example.com/page3.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>hourly</changefreq></url><url><loc>http://www.example.com/page4.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>daily</changefreq></url><url><loc>http://www.example.com/page5.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>weekly</changefreq></url><url><loc>http://www.example.com/page6.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>monthly</changefreq></url><url><loc>http://www.example.com/page7.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>yearly</changefreq></url><url><loc>http://www.example.com/page8.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>always</changefreq></url><url><loc>http://www.example.com/page9.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>never</changefreq></url></urlset>"

def test_sitemap_file_with_indent ():
  sitemap_file = SitemapFile(TEST_DIR.joinpath("sample.xml"), [
    ("http://www.example.com/page.html", datetime.datetime(2025, 1, 23), 0.5, ChangeFreq.NONE),
    ("http://www.example.com/page2.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.NONE),
    ("http://www.example.com/page3.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.HOURLY),
    ("http://www.example.com/page4.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.DAILY),
    ("http://www.example.com/page5.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.WEEKLY),
    ("http://www.example.com/page6.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.MONTHLY),
    ("http://www.example.com/page7.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.YEARLY),
    ("http://www.example.com/page8.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.ALWAYS),
    ("http://www.example.com/page9.html", datetime.datetime(2025, 1, 23), 1.0, ChangeFreq.NEVER),
  ])
  sitemap_file.save(use_indent=True)
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == """<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
  <url>
    <loc>http://www.example.com/page2.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
  </url>
  <url>
    <loc>http://www.example.com/page3.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>hourly</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page4.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>daily</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page5.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>weekly</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page6.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>monthly</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page7.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>yearly</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page8.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>always</changefreq>
  </url>
  <url>
    <loc>http://www.example.com/page9.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>never</changefreq>
  </url>
</urlset>"""
