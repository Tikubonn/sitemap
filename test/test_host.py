
import pytest
from pathlib import Path
from sitemap import Host

def test_host ():
  host = Host("http", "www.example.com", "./")
  assert host.scheme == "http"
  assert host.netloc == "www.example.com"
  assert host.root_dir == Path("./")
  assert host.path_to_url("./", params="", query="a=b&c=d", fragment="e") == "http://www.example.com/?a=b&c=d#e"
  assert host.path_to_url("./sample", params="", query="a=b&c=d", fragment="e", is_dir=False) == "http://www.example.com/sample?a=b&c=d#e"
  assert host.path_to_url("./sample", params="", query="a=b&c=d", fragment="e", is_dir=True) == "http://www.example.com/sample/?a=b&c=d#e"
