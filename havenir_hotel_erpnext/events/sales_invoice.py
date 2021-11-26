import frappe
from frappe import _
from havenir_hotel_erpnext.api.doctype import get_table_seats

def validate(doc, event):
    # validate table seat
    if(doc.restaurant_tables):
        tables = 0
        selected_tables = [table.table for table in doc.restaurant_tables]

        # clear removed tables
        cur_invoice_tables = frappe.db.sql(f"""
             SELECT rt.name FROM `tabRestaurant Tables` rt
             WHERE rt.occupied=1 AND rt.party="{doc.doctype}" AND rt.party_name="{doc.name}"
         ;""", as_dict=True)
        for i in cur_invoice_tables:
            if not(i.name in selected_tables):
                table_doc = frappe.get_doc('Restaurant Tables', i.name)
                table_doc.occupied = 0
                table_doc.save()

        # release seats
        occupied_tables = [i.name for i in frappe.db.sql(f"""
            SELECT rt.name FROM `tabRestaurant Tables` rt
            WHERE rt.occupied=1 AND rt.party!="{doc.doctype}" AND rt.party_name!="{doc.name}"
        ;""", as_dict=True)]

        for i in doc.restaurant_tables:
            if not(i.table in occupied_tables):
                # release
                table_doc = frappe.get_doc('Restaurant Tables', i.table)
                table_doc.db_set('party', doc.doctype)
                table_doc.db_set('party_name', doc.name)
                table_doc.occupied = 1
                table_doc.save()
            else:
                table_doc = frappe.get_doc('Restaurant Tables', i.table)
                frappe.throw(_(f"""Table <b>{i.table}</b> is currently occupied by \
                    <b>{table_doc.party}: \
                    <a href='/app/{table_doc.party.replace(' ', '-').lower()
                    }/{table_doc.party_name}'>{table_doc.party_name}</a></b> \
                    Please release table first before reassignment"""))
    
    if doc.split_bill_by and len(doc.items) > 0 and doc.grand_total > 0:
        if doc.split_bill_by=='Table' and doc.restaurant_tables.length > 0:
            doc.bill_per_table = doc.grand_total / len(doc.restaurant_tables)
        else:
            doc.bill_per_table = 0
    else:
        doc.bill_per_table = 0
    
    if doc.how_many_individuals and int(doc.how_many_individuals) > 0 and doc.grand_total > 0:
        doc.bill_per_individual = doc.grand_total / int(doc.how_many_individuals)
    else:
        doc.bill_per_individual = 0



    # frappe.db.commit()

        # end vaildate table seats


@frappe.whitelist()
def release_all(**kwargs):
	released = frappe.db.sql(f"""
		UPDATE `tabRestaurant Table Seat` r
		SET r.party='', r.party_name='', r.status='Free'
		WHERE r.table="{kwargs.get('table')}"
	;""")
	frappe.db.commit()
	frappe.msgprint(_("All seats released."))

@frappe.whitelist()
def get_seats(self):
	seats =  [i.name for i in frappe.db.sql(f"""
		SELECT r.name FROM `tabRestaurant Table Seat` r
		WHERE r.table="{self.name}" AND r.status='Occupied'
	;""", as_dict=1)]

	print(seats, '\n\n\n')
	return seats

@frappe.whitelist()
def release_seat(**kwargs):
	seat = frappe.form_dict.seat or kwargs.get('seat')
	print(seat, '\n\n')
	frappe.db.sql(f"""
		UPDATE `tabRestaurant Table Seat` r
		SET r.party='', r.party_name='', r.status='Free'
		WHERE r.name="{seat}"
	;""")
	frappe.db.commit()
	return True
