import frappe


@frappe.whitelist()
def render():
	checked_in = frappe.db.sql("""
		SELECT COUNT(room_status) as checked_in
		FROM `tabRooms` WHERE room_status='Checked In';
	;""", as_dict=1)[0]

	reserved = frappe.db.sql("""
		SELECT COUNT(room_status) as reserved
		FROM `tabRooms` WHERE room_status='Reserved';
	;""", as_dict=1)[0]

	available = frappe.db.sql("""
		SELECT COUNT(room_status) as available
		FROM `tabRooms` WHERE room_status='Available';
	;""", as_dict=1)[0]

	room_service = frappe.db.sql("""
		SELECT COUNT(room_status) as room_service
		FROM `tabRooms` WHERE room_status='Room Service';
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
		'checked_in': checked_in,
		'reserved': reserved,
		'room_service': room_service,
		'available': available,
		'house_keeping': frappe.render_template(
			"havenir_hotel_erpnext/templates/includes/hotel_dashboard/housekepping_tbody.html",
			context={'house_keeping':house_keeping})
		}
