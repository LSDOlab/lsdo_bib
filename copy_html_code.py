from utils.html_writer import HTMLWriter
from utils.load_bib_data import load_bib_data_dict


mode = 'by journal/conference'
mode = 'by year'


html_writer = HTMLWriter()
html_writer.write_header()

if mode is 'by journal/conference':
    bib_data_dict = load_bib_data_dict(lsdo_journal=True)
    html_writer.write_lines_by_type(html_writer, 'journal')

    bib_data_dict = load_bib_data_dict(lsdo_conference=True)
    html_writer.write_lines_by_type(bib_data_dict, 'conference')
elif mode is 'by year':
    bib_data_dict = load_bib_data_dict(lsdo_conference=True, lsdo_journal=True)
    html_writer.write_lines_by_year(bib_data_dict)

html_writer.copy2clipboard()