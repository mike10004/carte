#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 28, 2014

@author: mchaberski
'''

import logging
from argparse import ArgumentParser
import csv
import glob
from jinja2 import Environment, PackageLoader
import os.path
import os

_log = logging.getLogger('prepareposts')

POST_TEMPLATES_DIR = '_posts_templates'
POST_SOURCES_DIR = '_posts_sources'

env = Environment(loader=PackageLoader('prepareposts', POST_TEMPLATES_DIR))

def format_parameters_element(parameters_str):
  if parameters_str:
    _log.debug("formatting parameters string %s", repr(parameters_str))
    parameters = []
    for parameter_str in parameters_str.split("\n"):
      attributes = parameter_str.split(' ', 2)
      _log.debug("parsed parameter string %s into %d attributes", repr(parameter_str), len(attributes))
      pname, ptype, pdescription = attributes[0], '', ''
      if len(attributes) == 2:
        pdescription = attributes[1]
      elif len(attributes) == 3:
        ptype = attributes[1]
        pdescription = attributes[2]
      parameters.append({
        'name': pname,
        'type': ptype,
        'description': pdescription,
      })
    return parameters
  else:
    return []

def format_element(element, heading):
    if heading == 'query_parameters':
      return format_parameters_element(element)
    elif heading == 'path_parameters':
      return format_parameters_element(element)
    else:
      return element

def format_row(rowdict):
  for k in rowdict:
    v = rowdict[k]
    v = format_element(v, k)
    rowdict[k] = v
  return rowdict

def load_content(kind, content_dir=POST_SOURCES_DIR):
  filename = os.path.join(content_dir, kind + 's.csv')
  try:
    with open(filename, 'r') as ifile:
      reader = csv.DictReader(ifile)
      rows = [format_row(row) for row in reader]
      transform = _get_content_transform(kind)
      if transform is not None: rows = transform(rows)
      return rows
  except IOError as ex:
    _log.warn(" %s not found (or reading it failed); no posts will be generated for kind '%s'", filename, kind)
    return []

AUTO_GENERATED_MARKER = 'x'

def construct_filename(content, kind, marker=AUTO_GENERATED_MARKER):
    year, month, day = tuple([int(content[k]) for k in ('year', 'month', 'day')])
    extension = os.path.splitext(_find_template_filename(kind))[1]
    if kind == 'endpoint':
      category = content['category'].lower().replace(' ', '-')
      method = content['method'].lower()
      return "%04d-%02d-%02d-%s-%s-%s%s" % (year, month, day, marker, method, category, extension)
    elif kind == 'type':
      type_name = content['type_name'].lower()
      return "%04d-%02d-%02d-%s-%s-%s%s" % (year, month, day, marker, 'type', type_name, extension)

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

_CONTENT_TRANSFORMS = {
  'endpoint': None,
  'type': coalesce_type_fields,
}

def _get_content_transform(kind):
  try:
    transform = _CONTENT_TRANSFORMS[kind]
  except KeyError:
    transform = None
  return transform

def render_contents(template, pagedefs, kind):
  for content in pagedefs:
      filename = construct_filename(content, kind)
      with open(os.path.join('_posts', filename), 'w') as ofile:
          rendered = template.render(content)
          ofile.write(rendered)
      print "created", filename

def load_kinds():
  template_files = glob.glob(os.path.join(POST_TEMPLATES_DIR, '*.*'))
  return [os.path.splitext(os.path.basename(f))[0] for f in template_files]

def _find_template_filename(kind):
  pattern = os.path.join(POST_TEMPLATES_DIR, kind + '.*')
  return os.path.basename(glob.glob(pattern)[0])

def clean_posts(marker=AUTO_GENERATED_MARKER):
  generated_posts = glob.glob('_posts/????-??-??-' + marker + '-*.*')
  for f in generated_posts:
    os.remove(f)
    _log.debug(" removed %s", f)
  _log.info(" %d posts cleaned", len(generated_posts))

def main():
  parser = ArgumentParser()
  parser.add_argument("--clean", action="store_true", help="delete generated posts before generating new ones")
  parser.add_argument("--log-level", choices=('debug', 'info', 'warn', 'error'), help="set logging level", default='info')
  parser.add_argument("--debug", action="store_const", dest="log_level", const='debug')
  args = parser.parse_args()
  logging.basicConfig(level=eval('logging.' + args.log_level.upper()))
  if args.clean:
    clean_posts()
  for kind in load_kinds():
    template = env.get_template(_find_template_filename(kind))
    pagedefs = load_content(kind)
    render_contents(template, pagedefs, kind)
  return 0

if __name__ == '__main__':
    exit(main())
