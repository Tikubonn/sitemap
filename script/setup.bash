#!/bin/bash

mkdir -v -p ./src/sitemap/static/xsd
wget -v -O ./src/sitemap/static/xsd/sitemap.xsd https://www.sitemaps.org/schemas/sitemap/09/sitemap.xsd
wget -v -O ./src/sitemap/static/xsd/sitemap-image.xsd https://www.google.com/schemas/sitemap-image/1.1/sitemap-image.xsd
wget -v -O ./src/sitemap/static/xsd/siteindex.xsd https://www.sitemaps.org/schemas/sitemap/siteindex.xsd
