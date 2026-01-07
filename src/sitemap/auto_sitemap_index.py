
import datetime
from typing import Generator
from pathlib import Path
from dataclasses import dataclass
from .abc import ISitemap, ISitemapFile
from .host import Host
from .sitemap_index import SitemapIndex

@dataclass
class AutoSitemapIndex (ISitemap):

  """複数の ISitemap オブジェクトから自動的にサイトマップインデックスを作成します。
  
  Attributes
  ----------
  host : Host
    適切に設定された `Host` オブジェクトです。
  file : Path
    作成されたサイトマップインデックスの保存先となるファイルパスです。
  sitemaps : list[ISitemap]
    作成されるサイトマップインデックスが参照する `ISitemap` オブジェクトのリストです。
  """

  host:Host
  file:Path
  sitemaps:list[ISitemap]

  def __post_init__ (self):
    self.file = Path(self.file)

  def save_files (self, use_indent:bool=False) -> Generator[ISitemapFile, None, None]:
    sitemap_index = SitemapIndex(self.file)
    for sitemap in self.sitemaps:
      for sitemap_file in sitemap.save_files(use_indent=use_indent):
        loc = self.host.path_to_url(sitemap_file.file)
        last_mod = datetime.datetime.fromtimestamp(sitemap_file.file.stat().st_mtime)
        sitemap_index.register(loc, last_mod)
        yield sitemap_file
    yield from sitemap_index.save_files(use_indent=use_indent)
    sitemap_index.close()
