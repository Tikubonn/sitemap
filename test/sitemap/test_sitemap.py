
import pytest
import shutil
import datetime
from io import StringIO
from pathlib import Path
from sitemap.sitemap import ChangeFreq, Sitemap, URL

TEST_DIR = Path("./.test")

def setup_function (function):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (function):
  shutil.rmtree(TEST_DIR)

#main

def test_sitemap_save ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0)
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.HOURLY)
  sitemap.register("http://www.example.com/page4.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.DAILY)
  sitemap.register("http://www.example.com/page5.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.WEEKLY)
  sitemap.register("http://www.example.com/page6.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.MONTHLY)
  sitemap.register("http://www.example.com/page7.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.YEARLY)
  sitemap.register("http://www.example.com/page8.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.ALWAYS)
  sitemap.register("http://www.example.com/page9.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.NEVER)
  assert [sitemap_file.file for sitemap_file in sitemap.save_files()] == [TEST_DIR.joinpath("sample.xml")]
  with open(TEST_DIR.joinpath("sample.xml"), "r") as file:
    assert file.read() == "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://www.example.com/page.html</loc><lastmod>2025-01-23</lastmod></url><url><loc>http://www.example.com/page2.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority></url><url><loc>http://www.example.com/page3.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>hourly</changefreq></url><url><loc>http://www.example.com/page4.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>daily</changefreq></url><url><loc>http://www.example.com/page5.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>weekly</changefreq></url><url><loc>http://www.example.com/page6.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>monthly</changefreq></url><url><loc>http://www.example.com/page7.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>yearly</changefreq></url><url><loc>http://www.example.com/page8.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>always</changefreq></url><url><loc>http://www.example.com/page9.html</loc><lastmod>2025-01-23</lastmod><priority>1.000</priority><changefreq>never</changefreq></url></urlset>"

def test_sitemap_save2 ():

  #未登録の Sitemap はファイルを作成しない。

  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  assert [sitemap_file.file for sitemap_file in sitemap.save_files()] == []

def test_sitemap_save_with_indent ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0)
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.HOURLY)
  sitemap.register("http://www.example.com/page4.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.DAILY)
  sitemap.register("http://www.example.com/page5.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.WEEKLY)
  sitemap.register("http://www.example.com/page6.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.MONTHLY)
  sitemap.register("http://www.example.com/page7.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.YEARLY)
  sitemap.register("http://www.example.com/page8.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.ALWAYS)
  sitemap.register("http://www.example.com/page9.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.NEVER)
  assert [sitemap_file.file for sitemap_file in sitemap.save_files(use_indent=True)] == [TEST_DIR.joinpath("sample.xml")]
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

def test_sitemap_get ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/not-found.html") is None

def test_sitemap_clear ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.clear()
  assert sitemap.get("http://www.example.com/page.html") is None
  assert sitemap.get("http://www.example.com/page2.html") is None
  assert sitemap.get("http://www.example.com/page3.html") is None
  assert sitemap.get("http://www.example.com/not-found.html") is None

def test_sitemap_unregister ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.unregister("http://www.example.com/page.html")
  sitemap.unregister("http://www.example.com/page2.html")
  sitemap.unregister("http://www.example.com/page3.html")
  assert sitemap.get("http://www.example.com/page.html") is None
  assert sitemap.get("http://www.example.com/page2.html") is None
  assert sitemap.get("http://www.example.com/page3.html") is None

def test_sitemap_unregister2 ():

  #未登録のデータを抹消した場合の動作確認

  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.unregister("http://www.example.com/not-found.html")
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/not-found.html") is None

def test_sitemap_list_all ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  sitemap.register("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page.html") == URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page2.html") == URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.get("http://www.example.com/page3.html") == URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23))
  assert sitemap.list_all() == [
    URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23)),
    URL("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23)),
    URL("http://www.example.com/page3.html", last_mod=datetime.datetime(2025, 1, 23)),
  ]

def test_sitemap_load ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  with StringIO("""<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
</urlset>
""") as stream:
    sitemap.load(stream)
  with StringIO("""<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
</urlset>
""") as stream:
    sitemap.load(stream)
  assert sitemap.list_all() == [
    URL("http://www.example.com/", last_mod=datetime.datetime(2025, 1, 23)),
    URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23)),
  ]

def test_sitemap_loads ():
  sitemap = Sitemap(TEST_DIR.joinpath("sample.xml"))
  sitemap.loads("""<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
</urlset>
""")
  sitemap.loads("""<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
</urlset>
""")
  assert sitemap.list_all() == [
    URL("http://www.example.com/", last_mod=datetime.datetime(2025, 1, 23)),
    URL("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23)),
  ]
