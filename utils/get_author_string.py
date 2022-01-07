def get_author_string(ref):
    line = ''

    authors_list = ref.persons.values()[0]
    for ind, author in enumerate(authors_list):

        first_names = ' '.join(author.bibtex_first_names)
        last_names = ' '.join(author.last_names)

        work = first_names

        # Turn all full words into single letters
        work = work.split(' ')
        for k in range(len(work)):
            if len(work[k]) > 1 and work[k][1] != '.':
                work[k] = work[k][0]
        work = ' '.join(work)

        # Remove all periods
        work = work.replace('.', '')

        # Replace all spaces with '. '
        work = work.split(' ')
        work = '. '.join(work)

        # Add a final period
        work = work + '.'

        first_names = work

        # Build string with the format, 'Last, First M.'
        name = last_names + ', ' + first_names

        # Append ' Last, First M.'
        line += ' '
        line += name
        line += ','

        # If second last entry, append ' and'
        if ind == len(authors_list) - 2:
            line += ' and'

    return line