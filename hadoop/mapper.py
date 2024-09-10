#!/usr/bin/env python

import sys
import csv

for line in sys.stdin:
    try:
        reader = csv.reader([line])
        for row in reader:
            review_score = row[6]

            if review_score:
                print('{0}'.format(review_score))
    except Exception as e:
        sys.stderr.write("Error processing line: {0} - {1}\n".format(line, str(e)))
        continue
