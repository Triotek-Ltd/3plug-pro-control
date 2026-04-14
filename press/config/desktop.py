# -*- coding: utf-8 -*-

from frappe import _


def get_data():
	return [
		{
			"module_name": "Press",
			"category": "Modules",
			"color": "blue",
			"description": "Single-server control plane for benches, sites, jobs, and forensics",
			"icon": "octicon octicon-server",
			"type": "module",
			"label": _("3plug Control"),
			"reverse": 1,
		}
	]
