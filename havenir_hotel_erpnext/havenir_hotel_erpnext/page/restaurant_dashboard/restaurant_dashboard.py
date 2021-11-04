import frappe
from datetime import datetime


@frappe.whitelist()
def render(**kwargs):
	_dict = frappe.form_dict
	from_date = _dict.from_date or str(datetime.today().date())
	to_date = _dict.to_date or str(datetime.today().date())
	from_date = f"{from_date} 00:00:00"
	to_date = f"{to_date} 23:59:59"

	checked_in = frappe.db.sql(f"""
		SELECT COUNT(room_status) as checked_in
		FROM `tabRooms` WHERE modified BETWEEN '{from_date}' AND '{to_date}'
		AND room_status='Checked In'
	;""", as_dict=1)[0].checked_in

	reserved = frappe.db.sql(f"""
		SELECT COUNT(room_status) as reserved
		FROM `tabRooms` WHERE modified BETWEEN '{from_date}' AND '{to_date}'
		AND room_status='Reserved'
	;""", as_dict=1)[0].reserved

	available = frappe.db.sql(f"""
		SELECT COUNT(room_status) as available
		FROM `tabRooms` WHERE modified BETWEEN '{from_date}' AND '{to_date}'
		AND room_status='Available'

	;""", as_dict=1)[0].available

	room_service = frappe.db.sql(f"""
		SELECT COUNT(room_status) as room_service
		FROM `tabRooms` WHERE modified BETWEEN '{from_date}' AND '{to_date}'
		AND room_status='Room Service'
	;""", as_dict=1)[0].room_service



	house_keeping = frappe.db.sql(f"""
		SELECT rooms, teams, status FROM `tabHousekeeping`
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
		WHERE si.docstatus=1
		AND si.modified BETWEEN '{from_date}' AND '{to_date}'
	;""", as_dict=1)

# si.modified BETWEEN "{str(datetime.today()).split(' ')[0]} 00:00:01"
# AND "{str(datetime.today()).split(' ')[0]} 23:59:59"


	top_10_today = frappe.db.sql(f"""
		SELECT i.item_code, sum(i.qty) as qty
		FROM `tabSales Invoice Item` i JOIN
		`tabSales Invoice` s ON i.parent=s.name
		WHERE s.modified BETWEEN
		'{from_date}' AND '{to_date}'
		GROUP BY i.item_code ORDER BY qty DESC LIMIT 10;
	;""", as_dict=1)

	# 	sales table
	SALES_COUNT = []
	SALES_COUNT_DICT = {}
	SALES_VOLUME = []
	SALES_VOLUME_DICT = {}
	SALES_COUNT_TOTAL = {
		'am8': 0, 'am10': 0, 'pm12': 0,
		'pm2': 0, 'pm4': 0, 'pm6': 0,
		'pm8': 0,
	}
	SALES_VOLUME_TOTAL = {
		'am8': 0, 'am10': 0, 'pm12': 0,
		'pm2': 0, 'pm4': 0, 'pm6': 0,
		'pm8': 0,
	}

	SALESDATA = frappe.db.sql(f"""
		SELECT si.item_code, si.qty, si.amount, s.modified
		FROM `tabSales Invoice Item` si
		JOIN `tabSales Invoice` s ON si.parent=s.name
		WHERE s.modified BETWEEN '{from_date}' AND '{to_date}'
		AND s.docstatus=1 ORDER BY si.item_code ASC;
	;""", as_dict=1)

	for i in SALESDATA:
		if(SALES_COUNT_DICT.get(i.item_code)):
			pass
		else:
			SALES_COUNT_DICT[i.item_code] = {
				'item_code':i.item_code,
				'am8': 0, 'am10': 0, 'pm12': 0,
				'pm2': 0, 'pm4': 0, 'pm6': 0,
				'pm8': 0,
			}
			SALES_VOLUME_DICT[i.item_code] = {
				'item_code':i.item_code,
				'am8': 0, 'am10': 0, 'pm12': 0,
				'pm2': 0, 'pm4': 0, 'pm6': 0,
				'pm8': 0,
			}

		sales_time = i.modified.hour
		if(sales_time<=9):
			SALES_COUNT_DICT[i.item_code]['am8'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['am8'] += i.amount
			SALES_COUNT_TOTAL['am8'] += i.qty
			SALES_VOLUME_TOTAL['am8'] += i.amount
		elif(sales_time<=11):
			SALES_COUNT_DICT[i.item_code]['am10'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['am10'] += i.amount
			SALES_COUNT_TOTAL['am10'] += i.qty
			SALES_VOLUME_TOTAL['am10'] += i.amount
		elif(sales_time<=13):
			SALES_COUNT_DICT[i.item_code]['pm12'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['pm12'] += i.amount
			SALES_COUNT_TOTAL['pm12'] += i.qty
			SALES_VOLUME_TOTAL['pm12'] += i.amount
		elif(sales_time<=15):
			SALES_COUNT_DICT[i.item_code]['pm2'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['pm2'] += i.amount
			SALES_COUNT_TOTAL['pm2'] += i.qty
			SALES_VOLUME_TOTAL['pm2'] += i.amount
		elif(sales_time<=17):
			SALES_COUNT_TOTAL['pm4'] += i.qty
			SALES_VOLUME_TOTAL['pm4'] += i.amount
		elif(sales_time<=19):
			SALES_COUNT_DICT[i.item_code]['pm6'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['pm6'] += i.amount
			SALES_COUNT_TOTAL['pm6'] += i.qty
			SALES_VOLUME_TOTAL['pm6'] += i.amount
		else:
			SALES_COUNT_DICT[i.item_code]['pm8'] += i.qty
			SALES_VOLUME_DICT[i.item_code]['pm8'] += i.amount
			SALES_COUNT_TOTAL['pm8'] += i.qty
			SALES_VOLUME_TOTAL['pm8'] += i.amount


	# move sales data to list
	for i, j in SALES_COUNT_DICT.items():
		SALES_COUNT.append(j)
	for i, j in SALES_VOLUME_DICT.items():
		SALES_VOLUME.append(j)


	context = {
		'table_occupancy_percent': round(
			t_occupancy_percent, 2),
		'table_occupancy_vancant': round(t_free_percent, 2),
		'total_sales': frappe.format(total_sales[0].total, 'Currency'),
		'total_sales_volume': frappe.format(total_sales[0].qty, 'Float'),
		'is_takeout': frappe.format(total_sales[0].is_takeout, 'Float'),
		'top_10_today': top_10_today,
		'SALES_COUNT': SALES_COUNT,
		'SALES_VOLUME': SALES_VOLUME,
		'SALES_COUNT_TOTAL': [SALES_COUNT_TOTAL],
		'SALES_VOLUME_TOTAL': [SALES_VOLUME_TOTAL],
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
