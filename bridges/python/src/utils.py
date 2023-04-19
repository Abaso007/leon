#!/usr/bin/env python
# -*- coding:utf-8 -*-

from json import loads, dumps
from pathlib import Path
from random import choice
from vars import useragent
from tinydb import TinyDB, Query, table, operations
from time import sleep
import sys
import os
import requests
import re

dirname = os.path.dirname(os.path.realpath(__file__))

intent_object_path = sys.argv[1]
codes = []

with open(intent_object_path, 'r', encoding = 'utf8') as intent_obj_file:
	intent_obj = loads(intent_obj_file.read())

def get_intent_obj():
	"""Return intent object"""

	return intent_obj

def translate(key, dict = { }):
	"""Pickup the language file according to the cmd arg
	and return the value according to the params"""

	# "Temporize" for the data buffer ouput on the core
	sleep(0.1)

	output = ''
	with open(os.path.join(os.getcwd(), 'skills', intent_obj['domain'], intent_obj['skill'], 'config', intent_obj['lang'] + '.json'), 'r', encoding = 'utf8') as file:
		obj = loads(file.read())
	# In case the key is a raw answer
	if key not in obj['answers']:
		return key

	prop = obj['answers'][key]
	variables = obj['variables'] if 'variables' in obj else { }
	output = choice(prop) if isinstance(prop, list) else prop
	if dict:
		for key in dict:
			output = output.replace(f'%{key}%', str(dict[key]))

	if variables:
		for key in variables:
			output = output.replace(f'%{key}%', str(variables[key]))

	return output

def output(type, content = '', core = { }):
	"""Communicate with the core"""

	if isinstance(content, dict):
		speech = translate(content['key'], content['data'])
		codes.append(content['key'])
	else:
		content = str(content)
		speech = translate(content)
		codes.append(content)

	print(dumps({
		'domain': intent_obj['domain'],
		'skill': intent_obj['skill'],
		'action': intent_obj['action'],
		'lang': intent_obj['lang'],
		'utterance': intent_obj['utterance'],
		'entities': intent_obj['entities'],
		'slots': intent_obj['slots'],
		'output': {
			'type': type,
			'codes': codes,
			'speech': speech,
			'core': core,
			'options': config('options')
		}
	}))

	if (type == 'inter'):
		sys.stdout.flush()

def http(method, url, headers = None):
	"""Send HTTP request with the Leon user agent"""

	session = requests.Session()
	session.headers.update({ 'User-Agent': useragent, 'Cache-Control': 'no-cache' })

	if headers != None:
	  session.headers.update(headers)

	return session.request(method, url)

def config(key):
	"""Get a skill configuration value"""

	with open(os.path.join(os.getcwd(), 'skills', intent_obj['domain'], intent_obj['skill'], 'src/config.json'), 'r', encoding = 'utf8') as file:
		obj = loads(file.read())
	return obj['configurations'][key]

def create_dl_dir():
	"""Create the downloads folder of a current skill"""

	dl_dir = os.path.join(os.getcwd(), 'downloads')
	# dl_dir = os.path.dirname(os.path.realpath(__file__)) + '/../../../../downloads/'
	skill_dl_dir = os.path.join(dl_dir, intent_obj['domain'], intent_obj['skill'])

	Path(skill_dl_dir).mkdir(parents = True, exist_ok = True)

	return skill_dl_dir

def db(db_type = 'tinydb'):
	"""Create a new dedicated database
	for a specific skill"""

	if db_type == 'tinydb':
		ext = '.json' if os.environ.get('LEON_NODE_ENV') != 'testing' else '.spec.json'
		db = TinyDB(
			os.path.join(
				os.getcwd(),
				'skills',
				intent_obj['domain'],
				intent_obj['skill'],
				f'memory/db{ext}',
			)
		)
		return {
			'db': db,
			'query': Query,
			'table': table,
			'operations': operations
		}

def get_table(slug):
	"""Get a table from a specific skill"""

	domain, skill, table = slug.split('.')
	ext = '.json' if os.environ.get('LEON_NODE_ENV') != 'testing' else '.spec.json'
	db = TinyDB(
		os.path.join(os.getcwd(), 'skills', domain, skill, f'memory/db{ext}')
	)
	return db.table(table)
