# mediawiki-export
Export MediaWiki categories for archiving purposes.

This script takes a list of categories, looks up those categories in
your wiki's API, and then exports each page of those categories to text
files.

These files get archived into a directory and tarball:

* wiki-export-YYYY-MM-DD/
* wiki-export-YYYY-MM-DD.tar.gz

All within the base directory at `/var/backups/wiki/`.

## Usage
In the script, set CATEGORIES and API_URL to the appropriate values. Then run the script. Set it up as a cron job if you want.
