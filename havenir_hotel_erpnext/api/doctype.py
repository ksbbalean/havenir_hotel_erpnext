import frappe


@frappe.whitelist()
def get_table_seats(**kwargs):
    table = frappe.form_dict.table or kwargs.get('table')
    seats = frappe.db.sql(f"""
        SELECT rrs.* FROM `tabRestaurant Table Seat` rrs
        WHERE rrs.table='{table}' AND rrs.status="Free"
    ;""", as_dict=1)

    return seats


@frappe.whitelist()
def get_tableinvoice_seats(**kwargs):
    table = frappe.form_dict.table or kwargs.get('table')
    party = frappe.form_dict.party or kwargs.get('party')
    party_name = frappe.form_dict.party_name or kwargs.get('party_name')
    seats = frappe.db.sql(f"""
        SELECT rrs.* FROM `tabRestaurant Table Seat` rrs
        WHERE rrs.table='{table}' AND rrs.party in ('{party}', '')
        AND rrs.party_name IN ('{party_name}', '')
    ;""", as_dict=1)

    return seats

@frappe.whitelist()
def get_table_seats_in_invoice(**kwargs):
    table = frappe.form_dict.seat_filter or kwargs.get('seat_filter')
    # doctype = frappe.form_dict.doctype or kwargs.get('doctype')
    # docname = frappe.form_dict.docname or kwargs.get('docname')

    seats = frappe.db.sql(f"""
        SELECT rrs.* FROM `tabRestaurant Table Seat` rrs
        WHERE {seat_filter}
    ;""", as_dict=1)

    # print(seats)
    return seats

@frappe.whitelist()
def setsi_table_filter(doctype, txt, searchfield, start, page_len, filters):
    # filter restauarant table for invoice
    # print(doctype, txt, searchfield, start, page_len, filters)
    occupied = filters.get('occupied')
    docname = filters.get('docname')
    doctype = filters.get('doctype')

    query = frappe.db.sql(f"""
        SELECT rt.name FROM `tabRestaurant Tables` rt
        WHERE rt.party_name="{docname}" OR rt.occupied=0
    ;""", as_list=1)
    # print(query)
    return query
    # (doctype,
    #         filters={
    #             'occupied': filters.get('occupied'),
    #             'party'
    #         },
    #         fields=['name'],
    #         order_by='name asc',
    #         as_list=True
    #     )
