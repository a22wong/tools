#!/usr/bin/env python
import requests
import nltk
import csv
from bs4 import BeautifulSoup, NavigableString

# get all urls to scrape from
urls = []
with open('urls_of_moe_speeches.csv', 'r') as f:
  reader = csv.reader(f)
  urls = list(reader)


# init progress utterance counters
nb_rows_so_far = 0
try:
    with open("moe_speeches.csv", 'r') as csvfile:
        nb_rows_so_far = sum(1 for row in csvfile)
except:
    pass

nb_urls = len(urls)
success_count = 0

# iterate to scrape
print(f'\n* scraping from %d urls' % nb_urls)
for i, url in enumerate(urls):
    print(f'* progress: (%d/%d)' % (i, nb_urls), end='\r')
    try:
        page = requests.get(url[0])
        soup = BeautifulSoup(page.text, "html.parser")

        # scrape and parse individal utterances
        utterances = []
        for found_tag in soup.find_all('p'):
            found_string = [element for element in found_tag if isinstance(element, NavigableString)]
            utts = nltk.sent_tokenize(found_string[0])
            utts = [utt for utt in utts if utt != ""]
            for utterance in utts:
                utterances.append(utterance.strip())

        # trim remaining unwanted lines (non-utterances)
        utterances = utterances[1:-3]

        # write to dataset
        with open("moe_speeches.csv", 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for utterance in utterances:
                wr.writerow([nb_rows_so_far+1, utterance])
                nb_rows_so_far += 1

        success_count += 1

    except KeyboardInterrupt:
        print("\n* terminating early")
        break

print(f'* %d/%d urls successfully scraped' % (success_count, nb_urls))

############################
# how to clean the dataset #
############################
#
# 1. exclude non-sentence utterances (i.e. "All rights reserved", "Copyright © 2018 Ministry of Education, Singapore", "Last updated:...")
#
# 2. exclude senteces with non-English content (i.e. Mandarin characters)
# 2a. non-English names are OK as long as they're transcribed with English alphabet [A-Za-z] characters only
#
# 3. check for characters that don't get encoded properly
#
