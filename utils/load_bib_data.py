from typing import OrderedDict
from six import iteritems

import bibtexparser
from pybtex.database.input import bibtex
import pybtex


def _remove_duplicate_entries(db):
    id_list = [entry['ID'] for entry in db.entries]

    unique_ids = set(id_list)
    counts = {id_:0 for id_ in unique_ids}

    new_entries = []
    for ind in range(len(db.entries)):
        id_ = id_list[ind]

        counts[id_] += 1
        if counts[id_] == 1:
            new_entries.append(db.entries[ind])

    db.entries = new_entries


def _load_entries(filename):
    with open(filename, 'r') as f:
        return bibtexparser.load(f)


def load_bib_data_dict(lsdo_journal=False, lsdo_conference=False, external=False):
    db = bibtexparser.bibdatabase.BibDatabase()
    if lsdo_journal:
        entries = _load_entries('raw_bib/lsdo_journal.bib').entries
        db.entries.extend(entries)
    if lsdo_conference:
        entries = _load_entries('raw_bib/lsdo_conference.bib').entries
        db.entries.extend(entries)
    if external:
        entries = _load_entries('raw_bib/external.bib').entries
        db.entries.extend(entries)

    _remove_duplicate_entries(db)

    # Convert the database object to a string
    bibtex_string = bibtexparser.dumps(db)

    # Convert the string to a bib data object
    bib_data = pybtex.database.parse_string(bibtex_string, 'bibtex')

    # Convert the bib data object to my own, simplified bib data dictionary
    bib_data_dict = OrderedDict()
    for entry in db.entries:
        key = entry['ID']
        bib_data_dict[key] = bib_data.entries[key]

    return bib_data_dict


def get_raw_bibtex_string(key, ref):
    bib_data = pybtex.database.BibliographyData({key: ref})
    bibtex_string = bib_data.to_string('bibtex')
    return bibtex_string