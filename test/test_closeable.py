
import pytest
from imageset import Closeable

def test_closeable ():

  #引数なしで実行した場合の基本機能の動作確認を行います

  closeable = Closeable()
  assert closeable.closed == False
  closeable.close()
  closeable.close()
  closeable.close()
  assert closeable.closed == True

def test_closeable_with_handler ():

  #引数を設定して実行した場合の基本機能の動作確認を行います

  closed_count = 0

  def on_close ():
    nonlocal closed_count
    closed_count += 1

  closeable = Closeable(on_close)
  assert closeable.closed == False
  closeable.close()
  closeable.close()
  closeable.close()
  assert closed_count == 1
  assert closeable.closed == True
