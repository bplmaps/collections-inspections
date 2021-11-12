import requests
import datetime
import csv

searchString = "https://collections.leventhalmap.org/search?f%5Bcollection_name_ssim%5D%5B%5D=American+Revolutionary+War-Era+Maps+%28Collection+of+Distinction%29"
fields = ["label_ssim","date_start_tsim","institution_name_ssim"]

complete = False
page = 1


with open("./scrape_results_{}.tsv".format(datetime.datetime.now()), 'w+') as outFile:

    outFile.write("id\t{}\n".format("\t".join(fields)))

    while not complete:

        r = requests.get("{}&format=json&per_page=100&page={}".format(searchString, page))

        thisPageResult = r.json()

        for doc in thisPageResult['response']['docs']:
            outFile.write(doc["id"])
            for f in fields:
                if isinstance(doc[f], list):
                    p = " || ".join(doc[f])
                else:
                    p = doc[f]
                outFile.write("\t{}".format(p))
            outFile.write("\n")


        complete = True if thisPageResult['response']['pages']['last_page?'] else False
        page = thisPageResult['response']['pages']['next_page']
