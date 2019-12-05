from __future__ import print_function
import os
import sys

TOP_DIR="dist"
dirs = []
for (dirpath, dirnames, filenames) in os.walk(TOP_DIR):
    if "index.html" in filenames:
        dirs.append(os.path.basename(dirpath))
dirs.sort()
# print(dirs)

file = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
for dn in dirs:
    file += """
    <url>
        <loc>https://go.isptutor.org/brm/%s/index.html</loc>
        <lastmod>2019-08-08</lastmod>
        <changefreq>weekly</changefreq>
    </url>""" % dn
file += '</urlset>'

with open(os.path.join(TOP_DIR, "sitemap.xml"), "w") as fh:
    fh.write(file)
