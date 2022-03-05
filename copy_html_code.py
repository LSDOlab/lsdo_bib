from utils.html_writer import HTMLWriter
from utils.load_bib_data import load_bib_data_dict


# mode = 'by journal/conference'
mode = 'by year'


lsdo_journal_keys = list(load_bib_data_dict(lsdo_journal=True).keys())
lsdo_conference_keys = list(load_bib_data_dict(lsdo_conference=True).keys())
lsdo_keys = lsdo_journal_keys + lsdo_conference_keys

full_bib_data_dict = load_bib_data_dict(lsdo_journal=True, lsdo_conference=True, external=True)

html_writer = HTMLWriter()
html_writer.write_header()

if mode is 'by journal/conference':
    html_writer.write_lines_by_type(full_bib_data_dict, lsdo_journal_keys, 'journal')
    html_writer.write_lines_by_type(full_bib_data_dict, lsdo_conference_keys, 'conference')
elif mode is 'by year':
    html_writer.write_lines_by_year(full_bib_data_dict, lsdo_keys)

html_writer.copy2clipboard()