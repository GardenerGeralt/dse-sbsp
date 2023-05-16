import numpy as np
import csv

with open('MaterialEnergy.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('MaterialEnergy.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        MatEn = {rows[0]:rows[1] for rows in reader}

