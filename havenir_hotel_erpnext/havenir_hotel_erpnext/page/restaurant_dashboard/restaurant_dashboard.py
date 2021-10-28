import frappe
from datetime import datetime


@frappe.whitelist()
def render():
	checked_in = frappe.db.sql("""
		SELECT COUNT(room_status) as checked_in
		FROM `tabRooms` WHERE room_status='Checked In';
	;""", as_dict=1)[0].checked_in

	reserved = frappe.db.sql("""
		SELECT COUNT(room_status) as reserved
		FROM `tabRooms` WHERE room_status='Reserved';
	;""", as_dict=1)[0].reserved

	available = frappe.db.sql("""
		SELECT COUNT(room_status) as available
		FROM `tabRooms` WHERE room_status='Available';
	;""", as_dict=1)[0].available

	room_service = frappe.db.sql("""
		SELECT COUNT(room_status) as room_service
		FROM `tabRooms` WHERE room_status='Room Service';
	;""", as_dict=1)[0].room_service



	house_keeping = frappe.db.sql("""
		SELECT rooms, teams, status FROM `tabHousekeeping`;
	;""", as_dict=1)

	table_occupancy_percent = frappe.db.sql(f"""
		SELECT IFNULL(COUNT(r.name), 0) as count
		FROM `tabRestaurant Table Seat` r
		WHERE r.status="Occupied"
		UNION
		SELECT IFNULL(COUNT(r.name), 0) as count
		FROM `tabRestaurant Table Seat` r;
	;""", as_dict=1)
	t_occupancy_percent = 0
	t_free_percent = 0
	try:
		t_occupied = table_occupancy_percent[0].count
		t_total = table_occupancy_percent[1].count
		if(not t_total):
			pass
		else:
			t_occupancy_percent = t_occupied/t_total
			t_free_percent = 1-t_occupancy_percent
	except Exception as e:
		pass

	total_sales = frappe.db.sql(f"""
		SELECT IFNULL(SUM(si.grand_total), 0) as total,
		IFNULL(SUM(si.total_qty), 0) as qty,
		IFNULL(SUM(si.is_takeout), 0) as is_takeout
		FROM `tabSales Invoice` si
		WHERE si.modified BETWEEN
		"{str(datetime.today()).split(' ')[0]} 00:00:01"
		AND "{str(datetime.today()).split(' ')[0]} 23:59:59"
		AND si.docstatus=1;
	;""", as_dict=1)

	top_10_today = frappe.db.sql(f"""
		SELECT i.item_code, sum(i.qty) as qty
		FROM `tabSales Invoice Item` i JOIN
		`tabSales Invoice` s ON i.parent=s.name
		WHERE s.modified BETWEEN
		'2021-01-01 00:00:01' AND '2021-10-31 23:59:59'
		GROUP BY i.item_code ORDER BY qty DESC LIMIT 10;
	;""", as_dict=1)

	context = {
		'table_occupancy_percent': round(
			t_occupancy_percent, 2),
		'table_occupancy_vancant': round(t_free_percent, 2),
		'total_sales': frappe.format(total_sales[0].total, 'Currency'),
		'total_sales_volume': frappe.format(total_sales[0].qty, 'Float'),
		'is_takeout': frappe.format(total_sales[0].is_takeout, 'Float'),
		'top_10_today': top_10_today,
		# 'checked_in': checked_in,
		# 'reserved': reserved,
		# 'room_service': room_service,
		# 'available': available,
	}
	template = frappe.render_template(
		"havenir_hotel_erpnext/havenir_hotel_erpnext/page/restaurant_dashboard/index.html",
		context=context)
	return {
		'template':template,
		**context
		}
