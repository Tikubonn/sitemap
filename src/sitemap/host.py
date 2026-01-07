
import urllib.parse
import importlib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Host:

  """ローカルパスから URL を作成する機能を提供します。

  Examples
  --------
  >>> host = Host("http", "www.example.com", "./")
  >>> host.path_to_url("./page.html")
  'http://www.example.com/page.html'

  Attributes
  ----------
  scheme : str
    作成される URL のスキーム部分の文字列です。
  netloc : str
    作成される URL のドメイン部分の文字列です。
  root_dir : Path
    作成される URL のパス部分の絶対パスの基準となるディレクトリです。
  """

  scheme:str
  netloc:str
  root_dir:Path

  def __post_init__ (self):
    self.root_dir = Path(self.root_dir)

  def path_to_url (self, path:Path|str, params:str="", query:str="", fragment:str="", is_dir:bool=False) -> str:

    """ローカルパスから URL を作成します。

    Notes
    -----
    引数 `path` がファイルであれば、引数 `is_dir` の値は無視されます。

    Parameters
    ----------
    path : Path|str
      URL に変換するパスです。
    params : str
      作成される URL の最後のパス要素に対するパラメータ部分の文字列です。
      未指定ならば空文字列が設定されます。
    params : str
      作成される URL のクエリ部分の文字列です。
      未指定ならば空文字列が設定されます。
    fragment : str
      作成される URL のフラグメント部分の文字列です。
      未指定ならば空文字列が設定されます。
    is_dir : bool
      引数 `path` がディレクトリであるかどうかを設定します。
      引数 `path` が存在せず設定値が真であればパスの末尾に "/" が添加されます。
      本引数が未指定ならば `False` が設定されます。

    Returns
    -------
    str
      作成された URL が返されます。
    """

    if Path(path) == self.root_dir:
      path_str = "/"
    else:
      path_str = Path("/").joinpath(Path(path).relative_to(self.root_dir)).as_posix()
      if is_dir or Path(path).is_dir():
        path_str += "/"
    return urllib.parse.urlunparse((
      self.scheme,
      self.netloc,
      path_str,
      params,
      query,
      fragment,
    ))
