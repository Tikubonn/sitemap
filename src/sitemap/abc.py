
from io import TextIOBase
from abc import ABC, abstractmethod
from typing import Generator
from pathlib import Path

class ISitemapFile (ABC):

  """サイトマップファイルを表現するための規格を提供します。"""

  @property
  @abstractmethod
  def file (self) -> Path:

    """登録されたサイトマップ情報の保存先となるファイルを返します。"""

    pass

  @abstractmethod
  def save (self, use_indent:bool=False):

    """登録されたサイトマップ情報を設定されたファイルに保存します。

    Parameters
    ----------
    use_indent : bool
      サイトマップ情報を保存する際にインデントを用いるかを設定します。
      未指定ならば `False` が設定されます。
    """

    pass

class ISitemap (ABC):

  """サイトマップを表現するための規格を提供します。"""

  @abstractmethod
  def save_files (self, use_indent:bool=False) -> Generator[ISitemapFile, None, None]:

    """自身に登録されたサイトマップ情報を保存します。

    Parameters
    ----------
    use_indent : bool
      サイトマップ情報を保存する際にインデントを用いるかを設定します。
      未指定ならば `False` が設定されます。

    Returns
    -------
    Generator[ISitemapFile, None, None]
      適切に分割され保存処理が行われた `ISitemapFile` の集合です。
    """

    pass

class ILoadable (ABC):

  """file-like, str オブジェクトから読み込んだ内容を自身に反映させるための規格を提供します。"""

  @abstractmethod
  def load (self, stream:TextIOBase):

    """file-like オブジェクトから読み込んだ内容を自身に反映させます。

    Parameters
    ----------
    stream : TextIOBase
      読み込み元となる file-like オブジェクトです。
    """

    pass

  @abstractmethod
  def loads (self, source:str):

    """str オブジェクトから読み込んだ内容を自身に反映させます。

    Parameters
    ----------
    source : str
      読み込み元になる str オブジェクトです。
    """

    pass
