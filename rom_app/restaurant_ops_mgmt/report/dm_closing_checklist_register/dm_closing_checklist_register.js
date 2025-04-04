frappe.query_reports["Dm Closing Checklist Register"] = {
"filters": [
		{
			"fieldname": "from_date_filter",
			"label": "From Date *",
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
			"mandatory": 1,
		},
		{
			"fieldname": "to_date_filter",
			"label": "To Date *",
			"fieldtype": "Date",
			"default": frappe.datetime.now_date(),
			"mandatory": 1,
		},
			{
			"fieldname": "branch_filter",
			"label": "Branch",
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "dm_close_child_yes",
			"label": "Dm Audit",
			"fieldtype": "Select",
			"options": "\nYes\nNo"
		},
		{
			"fieldname": "rm_audit_filter",
			"label": "Rm Audit",
			"fieldtype": "Select",
			"options": "\nYes\nNo"
		},
		{
			"fieldname": "question_filter",
			"label": "Question",
			"fieldtype": "Data",
		},
	]
};
