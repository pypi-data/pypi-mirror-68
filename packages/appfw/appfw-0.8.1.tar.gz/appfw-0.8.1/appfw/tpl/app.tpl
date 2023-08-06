#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


Created on   : {now} ( {author} )
Last modified: May 10, 2020, Sun 12:51:01 -0500
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from future.utils import raise_with_traceback # needs pip install future

import sys
import os
import os.path

import argparse
from appfw import app


def main(args, config):
    try:
        pass
    except Exception as e:
        # raise_with_traceback(e)
        app.exception(e)


def parse_args():
    parser = argparse.ArgumentParser(description='''{app_name}''')
    parser.add_argument('-c', '--cfgfile', default='{conf_file}',
                        type=str, help='Configuration file')
    parser.add_argument('--log-section', default='log', type=str,
                        help='Log section name in the configuration file')
    # parser.add_argument('-i', '--input', required=True, type=int,
    #					default=0, help='Input variable count')
    # parser.add_argument('categories', metavar='CATEGORY', nargs='+',
    #					help='a category for the accumulator')
    # parser.add_argument('-d', '--delete', action='store_true', required=False,
    #					help='Delete previous work, and restart')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    config = app.configure(args)
    main(args, config)
