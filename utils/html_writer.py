from six import iteritems
from contextlib import contextmanager
import pyperclip

from .get_author_string import get_author_string
from .load_bib_data import get_raw_bibtex_string


class HTMLWriter(object):

    def __init__(self):
        self.lines = []
        self.indentation = 0

    def remove_last_character(self):
        self.lines[-1] = self.lines[-1][:-2]

    def write_line(self, line, no_indent=False):
        if no_indent:
            prefix = ''
        else:
            prefix = ' ' * 4 * self.indentation
        # self.lines.append(prefix + line) # + r'\n')
        self.lines.append(prefix + line + '\n')

    def write_header(self):
        with open('raw_html/html_bib_header.html', 'r') as f:
            lines = f.readlines()

        self.lines.extend(lines)

        # for line in lines:
        #     self.write_line(line)

    def write_heading(self, heading_title):
        html_line = '<h3 id="h.p_wWsYqgOg8L8R" class="zfr3Q JYVBee">{}</h3>'.format(heading_title)
        self.write_line(html_line)

    def write_link(self, name, url):
        html_line = r'<a href="{}">{}</a>'.format(url, name)
        self.write_line(html_line)

    def write_quote(self, text):
        html_line = r'<q>{}</q>'.format(text)
        self.write_line(html_line)

    def write_italics(self, text):
        html_line = r'<i>{}</i>'.format(text)
        self.write_line(html_line)

    def write_button_dropdown(self, label, text_lines):
        # self.write_line('<button class="button dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">{}</button>'.format(label))
        with self.div('w3-dropdown-hover'):
            self.write_line('<button class="w3-button">{}</button>'.format(label))
            with self.div('w3-dropdown-content w3-bar-block w3-border'):
                self.write_line(r'<pre>')
                for line in text_lines:
                    self.write_line(line, no_indent=True)
                self.write_line(r'</pre>')

    def write_button_link(self, name, url):
        html_line = r'<a class="w3-button" href="{}">{}</a>'.format(url, name)
        self.write_line(html_line)

    def write_reference(self, key, ref):
        # Author and title
        self.write_line(get_author_string(ref))
        self.write_quote(ref.fields['title'] + ',')

        # Journal papers:
        if ref.type == 'article':
            if 'journal' in ref.fields:
                self.write_italics(ref.fields['journal'])
            if 'volume' in ref.fields:
                self.write_line(' Vol. {},'.format(ref.fields['volume']))
            if 'number' in ref.fields:
                self.write_line(' No. {},'.format(ref.fields['number']))
            if 'year' in ref.fields:
                self.write_line(' {},'.format(ref.fields['year']))
            if 'pages' in ref.fields:
                self.write_line(' pp. {},'.format(ref.fields['pages']))
            self.remove_last_character()

        # Conference papers:
        elif ref.type == 'inproceedings':
            if 'booktitle' in ref.fields:
                self.write_italics(ref.fields['booktitle'])
            if 'aiaa' in ref.fields:
                self.write_line(' (AIAA {}-{})'.format(ref.fields['year'], ref.fields['aiaa']))

        self.write_line(r'. &nbsp;')

        # doi
        doi = ref.fields.get('doi', None)
        if doi is not None and doi[:4] != 'http':
            doi = 'http://doi.org/{}'.format(doi)
        self.write_button_link('doi', doi)

        # bibtex
        bibtex_string = get_raw_bibtex_string(key, ref)
        bibtex_lines = bibtex_string.split(r'\n')
        self.write_button_dropdown('bibtex', bibtex_lines)

        # pdf
        pdf = ref.fields.get('pdf', None)
        if pdf is not None:
            self.write_button_link('pdf', pdf)

    def write_lines_by_type(self, bib_data_dict, keys, type_):
        if type_ is 'conference':
            heading = 'Conference papers'
            label = '[C{}]'
        elif type_ is 'journal':
            heading = 'Journal papers'
            label = '[J{}]'

        # Count number of journal/conference papers
        count = 0
        ref_types = {'journal': ('article',), 'conference': ('inproceedings',), 'both': ('article', 'inproceedings')}
        for ref_label, ref in iteritems(bib_data_dict):
            if ref_label in keys:
                if ref.type in ref_types[type_]:
                    count += 1

        ind_paper = count

        self.write_heading(heading)
        with self.enumerated_list():
            index = len(bib_data_dict)
            for ref_label, ref in iteritems(bib_data_dict):
                if ref_label in keys:
                    if ref.type in ref_types[type_]:
                        with self.bullet():
                            index -= 1
                            self.write_line(label.format(index))
                            self.write_reference(ref_label, ref)

    def write_lines_by_year(self, bib_data_dict, keys):
        years = []
        for ref_label, ref in iteritems(bib_data_dict):
            if ref_label in keys:
                year = ref.fields['year']
                if year not in years:
                    years.append(year)

        old_years = [int(year) for year in years] # convert to ints
        old_years.sort() # sort in place in ascending order
        new_years = old_years[::-1] # sort in descending order
        years = [str(year) for year in new_years] # convert back to strings

        for year in years:
            self.write_heading(year)
            with self.enumerated_list():
                for ref_label, ref in iteritems(bib_data_dict):
                    if ref_label in keys:
                        if ref.fields['year'] == year:
                            with self.bullet():
                                self.write_reference(ref_label, ref)

    @contextmanager
    def enumerated_list(self):
        self.write_line(r'<ul style="line-height:200%">')
        self.indentation += 1
        yield
        self.indentation -= 1
        self.write_line(r'</ul>')

    @contextmanager
    def bullet(self):
        self.write_line(r'<li>')
        self.indentation += 1
        yield
        self.indentation -= 1
        self.write_line(r'</li>')

    @contextmanager
    def div(self, div_class):
        self.write_line(r'<div class="{}">'.format(div_class))
        self.indentation += 1
        yield
        self.indentation -= 1
        self.write_line(r'</div>')

    def copy2clipboard(self):
        pyperclip.copy(r''.join(self.lines))