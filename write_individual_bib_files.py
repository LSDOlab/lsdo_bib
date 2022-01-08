from six import iteritems

from utils.load_bib_data import load_bib_data_dict
import pybtex
import bibtexparser


bibtex_string = \
r"""
<!DOCTYPE html>
<html>
<head>
<title>
Bibtex for {}
</title>
</head>
<body>
<pre>
{}
</pre>
</body>
</html>
"""

bib_data_dict = load_bib_data_dict(lsdo_conference=True, lsdo_journal=True)

for key, ref in iteritems(bib_data_dict):
    bib_database_ = pybtex.database.BibliographyData({key: ref})
    bib_string = bib_database_.to_string('bibtex')
    html_string = bibtex_string.format(key, bib_string[:-1])

    with open('generated_bib_files/{}.html'.format(key), 'w') as bibtex_file:
        bibtex_file.write(html_string)