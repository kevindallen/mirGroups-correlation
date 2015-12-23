import sys
import csv
import operator
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
groupnamesfile = "human_groups.txt"
grouphistfile_1 = "tanriverdi_seq/IonXpressRNA_013.group.hist"
grouphistfile_2 = "tanriverdi_seq/IonXpressRNA_014.group.hist"
thresh = 10
count_sum = 0
counts = {}

with open(groupnamesfile, 'rb') as f:
    for line in f:
    	counts[line.rstrip()] = [1, 1]

with open(grouphistfile_1, 'rb') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
    	if str(row[2]) != "count":
        	if int(row[2]) >= thresh:
        		counts[row[0]] = [int(row[2]), counts[row[0]][1]]
        		count_sum += int(row[2])
        		
with open(grouphistfile_2, 'rb') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
    	if str(row[2]) != "count":
        	if int(row[2]) >= thresh:
        		counts[row[0]] = [counts[row[0]][0], int(row[2])]


counts = {key:counts[key] for key in counts if counts[key] != [1, 1]}
sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))

#print sorted_counts
x = [i[1][0] for i in sorted_counts]
y = [i[1][1] for i in sorted_counts]
r = pearsonr(x, y)
print "Pearson correlation coefficient: ", r[0]
print "p-value: ", r[1]
plt.scatter(x, y, alpha=0.5)
plt.yscale('log')
plt.xscale('log')
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.show()