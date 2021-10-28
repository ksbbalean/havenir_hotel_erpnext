# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from havenir_hotel_erpnext.api.doctype import get_table_seats

class RestaurantTables(Document):

	def validate(self):
		# update seat installed
		seats = 0
		selected_seats = [seat.seat for seat in self.seats]
		deleted_seats = []
		seats_in_table = [seat.name for seat in get_table_seats(**{'table':self.name})]
		for seat in seats_in_table:
			if not seat in selected_seats:
				seat_doc = frappe.get_doc("Restaurant Table Seat", seat)
				if(seat_doc.table==self.name):
					seat_doc.db_set('table', '')
					deleted_seats.append(seat_doc.name)

		for seat in self.seats:
			error = 0
			try:
				seat_doc = frappe.get_doc("Restaurant Table Seat", seat.seat)
				if(seat_doc.table and (seat_doc.table!=self.name)):
					error = 1
				else:
					seat_doc.db_set('table', self.name)
					seats += 1
			except Exception as e:
				seats += 1
			if(error):
				frappe.throw(_(f"Seat <b>{seat.seat}</b> already assigned to table <b><a href='/app/restaurant-table/{seat_doc.table}'>{seat_doc.table}</a></b>, delete seat from the table before reasigning"))
		self.installed_seats = seats
