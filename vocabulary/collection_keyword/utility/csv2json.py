#!/usr/bin/env python

import json
import csv
import os
import sys
import argparse

# execute the main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert vocabulary keywords from CSV to JSON format')

    parser.add_argument('voc_name', help='name of the vocabulary')
    parser.add_argument('csv_input', help='path to the input CSV file in which vocabulary keywords are defined')
    parser.add_argument('json_output', help='path to the output JSON file')
    parser.add_argument('-d', '--delimiter',
                        action='store_const',
                        default=';',
                        const=str,
                        help='the delimiter between word and context reference id')

    args = parser.parse_args()

    if os.path.exists(args.csv_input):
        # read CSV file and convert into vocabulary dictionary
        csv_f = open(args.csv_input, 'r')
        #voc_dict = {'name': args.voc_name, 'keywords': []}
        voc_list = []
        row_id = 0
        for row in csv.reader(csv_f, delimiter=args.delimiter):
            row_id += 1
            if len(row) < 2:
                sys.stderr.write('insufficient data columns, line: %d' % row_id)
                continue
            ref = row[-1]
            key = args.delimiter.join(row[:-1])
            #voc_dict['keywords'].append( {'keyword':key, 'id':ref} )
            voc_list.append( {'keyword':key, 'id':ref} )
        csv_f.close()

        # dump vocabulary dictionary into JSON file
        json_f = open(args.json_output, 'w')
        #json.dump(voc_dict, json_f, indent=2, separators=(',',':'))
        json.dump(voc_list, json_f, indent=2, separators=(',',':'))
        json_f.close()

        exit(0)
    else:
        sys.stderr.write('file not found: %s' % args.csv_input)
        exit(1)



