frappe.pages['sample-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Sample Page',
		single_column: true
	});
}