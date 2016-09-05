#!/usr/bin/env python
import sys
import os
import re
import urllib2
import json
import zipfile
import operator
from jsonschema.validators import validate
from jsonschema.exceptions import ValidationError
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import getMyLogger

import argparse

if __name__ == "__main__":

    # command-line argument validators
    def valid_zipfile(s):
        if zipfile.is_zipfile(s):
            return s
        else:
            msg = "Invalid release file: %s" % s
            raise argparse.ArgumentTypeError(msg)

    parg = argparse.ArgumentParser(description='check availability of external urls defined in external_urls.json file', version="0.1")

    parg.add_argument('pkg_zipfile', type=valid_zipfile, help='path to the zipped package for release')

    parg.add_argument('-p', '--prefix',
                      action='store',
                      dest='url_prefix',
                      default='http://data.donders.ru.nl/doc',
                      help='prefix of the external_urls of which the documents should be provided by the rdm-ontology package. The external URLs matching this prefix will be cross-checked with the files right in this package')

    parg.add_argument('-i', '--index',
                      action='store',
                      dest='idx_file',
                      default='external_urls.json',
                      help='index file in the release package in which all external URLs are specified')

    parg.add_argument('-l', '--loglevel',
                      action='store',
                      dest='verbose',
                      type=int,
                      choices=[0, 1, 2, 3],
                      default=0,
                      help='set one of the following verbosity levels. 0|default:WARNING, 1:ERROR, 2:INFO, 3:DEBUG')

    args = parg.parse_args()
    logger = getMyLogger(name=os.path.basename(__file__), lvl=args.verbose)

    try:
        zf = zipfile.ZipFile(args.pkg_zipfile, 'r')
        all_files = zf.namelist()

        # check existence of external_urls.json
        if args.idx_file not in all_files:
            raise IOError('file not found: external_urls.json')

        f_urls = zf.open(args.idx_file, 'r')
        d_urls = json.load(f_urls)
        f_urls.close()

        bad_urls={}
        for k, v in sorted(d_urls.items(), key=operator.itemgetter(1)):
            if re.match('^%s' % args.url_prefix, v):
                # the URL matches url_prefix, should just check whether the file is provided by the package
                rel_fname = os.path.relpath(v, args.url_prefix)
                if rel_fname not in all_files:
                    logger.error("file not found for URL of %s: %s" % (k, rel_fname))
                    bad_urls[k] = v
                else:
                    logger.info("file found for URL of %s: %s" % (k, rel_fname))
            else:
                try:
                    connection = urllib2.urlopen(v)
                    code = connection.getcode()
                    connection.close()
                    logger.info("URL of %s: [%d] OK" % (k, code))
                except urllib2.URLError, e:
                    if e.getcode() == 403 and v[-1] == '/':
                        logger.warn("URL of %s: [%d] %s" % (k, e.getcode(), e.reason))
                    else:
                        logger.error("URL of %s: [%d] %s" % (k, e.getcode(), e.reason))
                        bad_urls[k] = v
                except urllib2.HTTPError, e:
                    logger.error("URL of %s: [%d] %s" % (k, e.getcode(), e.reason))
                    bad_urls[k] = v
    except IOError, e:
        pass
    else:
        pass
    finally:
        if zf:
            zf.close()

    # exit with proper code
    if bad_urls:
        sys.exit(1)
    else:
        sys.exit(0)