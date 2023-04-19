#!/usr/bin/env python
# -*- coding:utf-8 -*-

from time import time

import utils
from ..lib import db

def view_lists(params):
	"""View to-do lists"""

	# Lists number
	lists_nb = db.count_lists()

	# Verify if a list exists
	if lists_nb == 0:
		return utils.output('end', 'no_list')

	result = ''.join(
		utils.translate(
			'list_list_element',
			{
				'list': list_element['name'],
				'todos_nb': db.count_todos(list_element['name']),
			},
		)
		for list_element in db.get_lists()
	)
	return utils.output('end', { 'key': 'lists_listed',
		'data': {
			'lists_nb': lists_nb,
			'result': result
		}
	})
