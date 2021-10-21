import frappe


@frappe.whitelist()
def render():
	room_occupancy = frappe.db.sql("""
		SELECT COUNT(room_status) as occupied,
		COUNT(room_name) as total,
		COUNT(room_name)-COUNT(room_status) as free
		FROM `tabRooms` WHERE room_status='Checked In';
	;""", as_dict=1)[0]

	house_keeping = frappe.db.sql("""
		SELECT rooms, teams, status FROM `tabHousekeeping`;
	;""", as_dict=1)

	context = {
		'name': 'Ghorz'
	}
	template = frappe.render_template(
		"havenir_hotel_erpnext/templates/includes/hotel_dashboard/index.html",
		context=context)
	return {
		'template':template,
		'room_occupancy': room_occupancy,
		'house_keeping': frappe.render_template(
			"havenir_hotel_erpnext/templates/includes/hotel_dashboard/housekepping_tbody.html",
			context={'house_keeping':house_keeping})
		}
