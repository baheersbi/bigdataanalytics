#!/usr/bin/env python

import sys

highest_score = float('-inf')
lowest_score = float('inf')


for line in sys.stdin:
    line = line.strip()

    try:
        score = float(line)
        
        
        if score > highest_score:
            highest_score = score
        if score < lowest_score:
            lowest_score = score
    except ValueError:

        sys.stderr.write("Skipping invalid score: {0}\n".format(line))
        continue

print('Highest Score: {0}'.format(highest_score))
print('Lowest Score: {0}'.format(lowest_score))
