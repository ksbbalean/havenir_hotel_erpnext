import frappe


@frappe.whitelist()
def get_table_seats(**kwargs):
    table = frappe.form_dict.table or kwargs.get('table')
    print(kwargs, table, 'table\n\n')
    seats = frappe.db.sql(f"""
        SELECT rrs.* FROM `tabRestaurant Table Seat` rrs
        WHERE rrs.table='{table}' AND rrs.status="Free"
    ;""", as_dict=1)

    print(seats)
    return seats
