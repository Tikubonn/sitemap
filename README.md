
# sitemap

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

サイトマップを読み込み・作成するための機能を提供します。

## Usage

### Sitemap

`Sitemap` クラスを使用することでサイトマップを読み込み・書き込みすることができます。

> [!NOTE]
> なお、記録された URL の総数が 50,000 個を超えた場合、本クラスはそれらを複数のファイルに分割して保存する仕様になっています。

```py
import datetime
from sitemap import Sitemap, ChangeFreq

sitemap = Sitemap("./sample.xml")
sitemap.register("http://www.example.com/page.html", last_mod=datetime.datetime(2025, 1, 23))
sitemap.register("http://www.example.com/page2.html", last_mod=datetime.datetime(2025, 1, 23), priority=1.0, change_freq=ChangeFreq.HOURLY)
sitemap.save_files(use_indent=True)
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <lastmod>2025-01-23</lastmod>
  </url>
  <url>
    <loc>http://www.example.com/page2.html</loc>
    <lastmod>2025-01-23</lastmod>
    <priority>1.000</priority>
    <changefreq>hourly</changefreq>
  </url>
</urlset>
```

### Image Sitemap

`ImageSitemap` クラスを使用することで画像サイトマップを読み込み・書き込みすることができます。

> [!NOTE]
> こちらも `Sitemap` クラスと同様に、記録された URL の総数が 50,000 を越えた場合、それらを複数のファイルに分割して保存する仕様になっています。

```py
from sitemap import ImageSitemap

image_sitemap = ImageSitemap("./sample.xml")
image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image.png")
image_sitemap.register("http://www.example.com/page.html", "http://www.example.com/top-image2.png", image_caption="caption", image_geo_location="geo location", image_title="title", image_license="license")
image_sitemap.save_files(use_indent=True)
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>http://www.example.com/page.html</loc>
    <image:image>
      <image:loc>http://www.example.com/top-image.png</image:loc>
    </image:image>
    <image:image>
      <image:loc>http://www.example.com/top-image2.png</image:loc>
      <image:caption>caption</image:caption>
      <image:geo_location>geo location</image:geo_location>
      <image:title>title</image:title>
      <image:license>license</image:license>
    </image:image>
  </url>
</urlset>
```

### Sitemap Index

`SitemapIndex` クラスを使用することでサイトマップインデックスを読み込み・書き込みすることができます。

```py
import datetime
from sitemap import SitemapIndex

sitemap_index = SitemapIndex("./sample.xml")
sitemap_index.register("http://www.example.com/sitemap.xml", last_mod=datetime.datetime(2025, 1, 23))
sitemap_index.register("http://www.example.com/sitemap2.xml", last_mod=datetime.datetime(2025, 1, 23))
sitemap_index.register("http://www.example.com/sitemap3.xml", last_mod=datetime.datetime(2025, 1, 23))
sitemap_index.save_files(use_indent=True)
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
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
```

`AutoSitemapIndex` クラスを使用することで、複数の `ISitemap` オブジェクトからサイトマップインデックスを生成することができます。

> [!NOTE]
> 本クラスが初期化時に要求する `Host` インスタンスは、ローカルパスを URL に変換する機能を提供します。

```py
import datetime
from sitemap import AutoSitemapIndex, Sitemap, ImageSitemap, Host

host = Host("http", "www.example.com", "./")
sitemap = Sitemap("./sitemap.xml")
sitemap.register("http://www.example.com/", last_mod=datetime.datetime(2025, 1, 23))
image_sitemap = ImageSitemap("./image-sitemap.xml")
image_sitemap.register("http://www.example.com/", image_loc="http://www.example.com/top-image.png")
auto_sitemap_index = AutoSitemapIndex(host, "./sitemap-index.xml", [sitemap, image_sitemap])
auto_sitemap_index.save_files(use_indent=True)
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>http://www.example.com/image-sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
  <sitemap>
    <loc>http://www.example.com/sitemap.xml</loc>
    <lastmod>2025-01-23</lastmod>
  </sitemap>
</sitemapindex>
```

## Install

```shell
bash script/setup.py
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import sitemap

help(sitemap)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

sitemap licensed under the [AGPLv3](./LICENSE)[^1].

[^1]:ただし `script/setup.bash` により生成される `src/sitemap/static/xsd` 内ファイルの著作権はそれぞれの作者に帰属します。
