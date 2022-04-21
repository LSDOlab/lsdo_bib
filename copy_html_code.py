from utils.html_writer import HTMLWriter
from utils.load_bib_data import load_bib_data_dict


# -------------------- Options

# mode = 'by journal/conference'
mode = 'by year'

website = 'lsdo'
# website = 'uli'

# -------------------- Keys

lsdo_journal_keys = list(load_bib_data_dict(lsdo_journal=True).keys())
lsdo_conference_keys = list(load_bib_data_dict(lsdo_conference=True).keys())
lsdo_keys = lsdo_journal_keys + lsdo_conference_keys
uli_journal_keys = [
    'yan2022topology',
    'zhao2022open',
]
uli_conference_keys = [
]
uli_keys = uli_journal_keys + uli_conference_keys

if website is 'lsdo':
    journal_keys = lsdo_journal_keys
    conference_keys = lsdo_conference_keys
    keys = lsdo_keys
elif website is 'uli':
    journal_keys = uli_journal_keys
    conference_keys = uli_conference_keys
    keys = uli_keys

# -------------------- html_writer

full_bib_data_dict = load_bib_data_dict(lsdo_journal=True, lsdo_conference=True, external=True)

html_writer = HTMLWriter()
html_writer.write_header()

if mode is 'by journal/conference':
    html_writer.write_lines_by_type(full_bib_data_dict, journal_keys, 'journal')
    html_writer.write_lines_by_type(full_bib_data_dict, conference_keys, 'conference')
elif mode is 'by year':
    html_writer.write_lines_by_year(full_bib_data_dict, keys)

html_writer.copy2clipboard()