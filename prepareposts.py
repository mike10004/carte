#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 28, 2014

@author: mchaberski
'''

import csv
from jinja2 import Environment, PackageLoader
import os.path

POST_TEMPLATES_DIR = '_posts_templates'
POST_SOURCES_DIR = '_posts_sources'

env = Environment(loader=PackageLoader('prepareposts', POST_TEMPLATES_DIR))

def load_content(filename, content_dir=POST_SOURCES_DIR):
    with open(os.path.join(content_dir, filename), 'r') as ifile:
        reader = csv.DictReader(ifile)
        return [row for row in reader]

def construct_filename(content):
    year, month, day = tuple([int(content[k]) for k in ('year', 'month', 'day')])
    category = content['category'].lower()
    method = content['method'].lower()
    return "%04d-%02d-%02d-x-%s-%s.md" % (year, month, day, method, category)
    
def main():
    template = env.get_template('endpoint.md')
    pagedefs = load_content('endpoints.csv')
    for content in pagedefs:
        filename = construct_filename(content)
        with open(os.path.join('_posts', filename), 'w') as ofile:
            rendered = template.render(content)
            ofile.write(rendered)
        print "created", filename
    return 0

if __name__ == '__main__':
    exit(main())
