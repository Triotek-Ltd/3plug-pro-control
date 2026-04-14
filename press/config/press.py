from frappe import _


def get_data():
	return [
		{
			"label": _("Operations"),
			"items": [
				{"type": "doctype", "name": "Self Hosted Server"},
				{"type": "doctype", "name": "Server"},
				{"type": "doctype", "name": "Bench"},
				{"type": "doctype", "name": "Site"},
				{"type": "doctype", "name": "Release Group"},
			],
		},
		{
			"label": _("Execution"),
			"items": [
				{"type": "doctype", "name": "Agent Job"},
				{"type": "doctype", "name": "Ansible Play"},
				{"type": "doctype", "name": "Forensic Event"},
				{"type": "doctype", "name": "Press Job"},
			],
		},
		{
			"label": _("Applications"),
			"items": [
				{"type": "doctype", "name": "App"},
				{"type": "doctype", "name": "App Source"},
				{"type": "doctype", "name": "App Release"},
				{"type": "doctype", "name": "Deploy Candidate"},
			],
		},
		{
			"label": _("Analytics"),
			"items": [
				{"type": "doctype", "name": "Site Analytics"},
				{"type": "doctype", "name": "Analytics Server"},
			],
		},
		{
			"label": _("Team"),
			"items": [
				{"type": "doctype", "name": "Team"},
				{"type": "doctype", "name": "Account Request"},
			],
		},
		{
			"label": _("Settings"),
			"items": [
				{"type": "doctype", "name": "Press Settings"},
				{"type": "doctype", "name": "Site Plan"},
				{"type": "doctype", "name": "Custom Domain"},
				{"type": "doctype", "name": "Server Plan"},
			],
		},
	]
