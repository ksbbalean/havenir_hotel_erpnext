import frappe


@frappe.whitelist()
def render():
	context = {
		'name': 'Ghorz'
	}
	template = frappe.render_template(
		"havenir_hotel_erpnext/templates/includes/hotel_dashboard/index.html",
		context=context)
	return template
