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

def format_parameters_element(parameters_str):
  if parameters_str:
    parameters = []
    for parameter_str in parameters_str.split("\n"):
      attributes = parameter_str.split(' ', 3)
      pname = attributes[0]
      if len(attributes) == 2:
        ptype = ''
        pdescription = attributes[1]
      elif len(attributes) == 3:
        ptype = attributes[1]
        pdescription = attributes[2]
      parameters.append({
        'name': pname,
        'type': ptype,
        'description': pdescription,
      })
  else:
    return []

def format_element(element, heading):
    if heading == 'query_parameters':
      return format_parameters_element(element)
    elif heading == 'path_parameters'
      return format_parameters_element(element)

def format_row(rowdict):
  for k in rowdict:
    v = rowdict[k]
    v = format_element(v, k)
    rowdict[k] = v

def load_content(filename, content_dir=POST_SOURCES_DIR):
  try:
    with open(os.path.join(content_dir, filename), 'r') as ifile:
      reader = csv.DictReader(ifile)
      return [row for row in reader]
  except IOError as ex:
    print >> sys.stderr, ex
    print >> sys.stderr, 'skipping', filename
    return []

def construct_filename(content, kind):
    year, month, day = tuple([int(content[k]) for k in ('year', 'month', 'day')])
    if kind == 'endpoint':
      category = content['category'].lower()
      method = content['method'].lower()
      return "%04d-%02d-%02d-x-%s-%s.md" % (year, month, day, method, category)
    elif kind == 'type':
      type_name = content['type_name']
      return "%04d-%02d-%02d-x-%s-%s.md" % (year, month, day, 'type', type_name)

def _update_last(newvalue, lastvalue):
  if lastvalue is None:
    return newvalue
  return row[key] if row[key] else lastvalue

def coalesce_type_fields(pagedefs):
  typedefs = {}
  for row in pagedefs:
    type_name = row['type_name']
    if type_name not in typedefs:
      typedefs[type_name] = {
        'type_name': type_name,
        'summary': None,
        'fields': [],
      }
    typedef = typedefs[type_name]
    for k in row:
      if not k.startswith('field_'):
        typedef[k] = row[k] or typedef[k]
    typedef['fields'].append({
      'name': row['field_name'],
      'type': row['field_type'],
      'description': row['field_description'],
    })
  return list(typedefs.values())

def render_contents(template, pagedefs, kind):
  for content in pagedefs:
      filename = construct_filename(content, kind)
      with open(os.path.join('_posts', filename), 'w') as ofile:
          rendered = template.render(content)
          ofile.write(rendered)
      print "created", filename

def do_types():
  template = env.get_template('type.md')
  pagedefs = coalesce_type_fields(load_content('types.csv'))
  render_contents(template, page, 'type')

def do_endpoints():
  template = env.get_template('endpoint.md')
  pagedefs = load_content('endpoints.csv')
  render_contents(template, page, 'endpoint')

def main():
  do_types():
  do_endpoints()
  return 0

if __name__ == '__main__':
    exit(main())
