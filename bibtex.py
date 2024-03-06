import bibtexparser

def bibtex_to_bibitem(bibtex_file):
    def format_author(author):
        result = author.split(', ')[::-1]
        return ' '.join(result)
    
    with open(bibtex_file, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    bibitems = []
    for entry in bib_database.entries:
        authors = entry.get('author', '').split('  and\n')                            
        if len(authors) > 1:
            authors_formatted = f"{', '.join([format_author(x) for x in authors[:-1]])} and {format_author(authors[-1])}"            
        else:
            authors_formatted = f"{format_author(authors[0])}"                        
        title = entry.get('title', '')
        book_title = entry.get('booktitle', '')
        proceedings_prefix = ""
        if book_title.startswith("Proceedings"):
            proceedings_prefix = "In "
        year = entry.get('year', '')
        bibitem = f"\\bibitem{{{entry['ID']}}} {authors_formatted}, {year}, {title}, {proceedings_prefix}{{\\em {book_title}}}."
        bibitems.append(bibitem)

    return bibitems

# Example usage:
bibtex_file = 'references_paper1.bib'
bibtex_file_out = 'references_paper1.txt'
bibitems = bibtex_to_bibitem(bibtex_file)
with open(bibtex_file_out, 'w') as file:        
    for bibitem in bibitems:
        file.write(bibitem)
        file.write('\n\n')        
