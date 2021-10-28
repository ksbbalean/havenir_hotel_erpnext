import frappe
from frappe import _
from havenir_hotel_erpnext.api.doctype import get_table_seats

def validate(doc, event):
    # validate table seat
    if(doc.restaurant_table_seat):
        seats = 0
        selected_seats = [seat.seat for seat in doc.restaurant_table_seat]
        selected_seats_str = ""
        for i, j in enumerate(selected_seats):
            if(len(selected_seats)==i+1):
                selected_seats_str += f"'{j}'"
            else:
                selected_seats_str += f"'{j}', "
        # release seats
        invoice_seats_exists = frappe.db.sql(f"""
            SELECT r.* FROM `tabRestaurant Table Seat` r
            WHERE r.party="{doc.doctype}" AND r.party_name="{doc.name}"
        ;""", as_dict=True)
        for i in invoice_seats_exists:
            if not(i.name in selected_seats):
                # release
                seat_doc = frappe.get_doc('Restaurant Table Seat', i.name)
                seat_doc.db_set('party', '')
                seat_doc.db_set('party_name', '')
                seat_doc.status = 'Free'
                seat_doc.save()

        # process dict
        seats_in_table = frappe.db.sql(f"""
            SELECT r.* FROM `tabRestaurant Table Seat` r
            WHERE r.name in ({selected_seats_str})
        ;""", as_dict=1)
        for seat in seats_in_table:
            if((seat.party and seat.party_name) and
            (seat.party!=doc.doctype and seat.party_name!=doc.name)):
                print(seat.party, '\n\n\n')
                frappe.throw(_(f"""<b>{seat.name}</b> is currently held by \
                    <b>{seat.party}: \
                    <a href='/app/{seat.party.replace(' ', '-').lower()
                    }/{seat.party_name}'>{seat.party_name}</a></b> \
                    Please release seat first before reassignment"""))
            else:
                print(seat, '\n\n')
                seat_doc = frappe.get_doc('Restaurant Table Seat', seat.name)
                seat_doc.party = doc.doctype
                seat_doc.party_name = doc.name
                seat_doc.status = 'Occupied'
                seat_doc.save()

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
