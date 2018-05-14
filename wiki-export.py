#!/usr/bin/env python3
#
# wiki-export.py
#
# This script exports categories of pages from our MediaWiki to a
# directory of text files, archived into a tarball. See the README
# for more info.
#

from datetime import datetime
import os
from os.path import join
import requests
import shutil
from urllib.parse import urlencode
import xml.etree.ElementTree as ET


# The categories to export.
CATEGORIES = []

# Link to your MediaWiki's api.php
API_URL = ''

OUTPUT_BASE = '/var/backups/wiki/'

# The temporary output directory. This actually gets created and removed
# within this script, so its name doesn't really matter.
OUTPUT_DIR = 'out'


ns = {
    'ns': 'http://www.mediawiki.org/xml/export-0.10/',
}


def export_pages(category, page_titles):
    args = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'list': '',
        'meta': '',
        'export': 1,
        'exportnowrap': 1,
        'titles': '|'.join(page_titles),
    }
    url = '{}?{}'.format(API_URL, urlencode(args))
    r = requests.get(url)

    root = ET.fromstring(r.text)

    pages = root.findall('.//ns:page', ns)
    for page in pages:
        # Use this title for the filename
        title = page.find('ns:title', ns).text

        # Get the revision - this contains the latest page content.
        revision = page.find('ns:revision', ns)
        text = revision.find('ns:text', ns).text

        fname = join(OUTPUT_BASE, OUTPUT_DIR, category, title)
        print('Writing to {}...'.format(fname))
        with open(fname + '.txt', 'w') as f:
            f.write('{}\n\n'.format(title))
            f.write(text)


def export_category(category):
    """
    Given a category name, create a directory, and all the pages
    it contains inside that directory.

    The path is prefixed with out/
    """
    args = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': 'Category:{}'.format(category),
        # By default, it looks like the API limits the number of pages
        # returned to 10. I've increased this to 400. I don't think
        # we're exporting any categories larger than that.
        'cmlimit': 400,
        'format': 'json',
    }
    url = '{}?{}'.format(API_URL, urlencode(args))

    r = requests.get(url)
    data = r.json()

    # Make a file for each page in this category in the new
    # directory.
    pages = data.get('query').get('categorymembers')
    page_titles = [page.get('title') for page in pages]
    export_pages(category, page_titles)


def archive_output(directory_name):
    fname = 'wiki-export-{}'.format(datetime.today().strftime('%Y-%m-%d'))
    shutil.rmtree(join(OUTPUT_BASE, fname), True)
    shutil.move(join(OUTPUT_BASE, directory_name), join(OUTPUT_BASE, fname))
    shutil.make_archive(join(OUTPUT_BASE, fname), 'gztar', OUTPUT_BASE, fname)


def main():
    print('Exporting these categories:')
    print(CATEGORIES)

    try:
        os.mkdir(join(OUTPUT_BASE, OUTPUT_DIR))
    except FileExistsError:
        pass

    for category in CATEGORIES:
        try:
            os.mkdir(join(OUTPUT_BASE, OUTPUT_DIR, category))
        except FileExistsError:
            pass
        export_category(category)

    archive_output(OUTPUT_DIR)


if __name__ == '__main__':
    main()
