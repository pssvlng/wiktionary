import os
import mwxml
import mwparserfromhell

# Assuming 'your_german_wiktionary_dump.xml' is the path to your German Wiktionary XML dump
dump = mwxml.Dump.from_file(open(f'{os.path.expanduser("~")}/MyData/wiktionary/dewiktionary-20231101-pages-meta-current.xml'))

# Set to store unique "wortart" values
wortart_set = set()

# Iterate through pages in the dump
cntr = 0
for page in dump:
    # Iterate through revisions of the page
    cntr += 1
    if cntr % 1000 == 0:
        print(f"{cntr} records of processed")
    for revision in page:
        # Accessing wikitext content
        wikitext = revision.text

        # Parse wikitext using mwparserfromhell
        parsed_wikicode = mwparserfromhell.parse(wikitext)

        # Iterate through templates or other structures to find "wortart" values
        for template in parsed_wikicode.filter_templates():
            # Check for a template related to part of speech, adjust as needed
            if template.name.lower() in ["wortart", "pos"]:
                # Extract the value, assuming it's in the first parameter
                wortart_value = template.get("1").value.strip()

                # Add the value to the set
                wortart_set.add(wortart_value)

# Print the unique "wortart" values
print("Unique Wortart Values:")
for wortart in wortart_set:
    print(wortart)