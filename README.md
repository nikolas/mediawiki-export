# mediawiki-export
Export MediaWiki categories for archiving purposes.

This script takes a list of categories, looks up those categories on
wiki.ctl's API, and then exports each page of those categories to text
files.

These files get archived into a directory and tarball:

* wiki-export-YYYY-MM-DD/
* wiki-export-YYYY-MM-DD.tar.gz

All within the base directory at `/var/backups/wiki/`.
