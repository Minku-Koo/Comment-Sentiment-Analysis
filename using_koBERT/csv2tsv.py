import csv
 
filename = "comment-labeling"
csvName = filename+".csv"
tsvName = filename+"-.tsv"

with open(csvName,'r', encoding='utf-8') as csvin, open(tsvName, 'w', newline='', encoding='utf-8') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter='\t')
 
    for row in csvin:
        tsvout.writerow(row)