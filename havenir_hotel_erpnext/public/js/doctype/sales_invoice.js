frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// your code here
        if(!frm.is_new()){
            frm.add_custom_button('All Seats', () => {
                frappe.call({
                    method: "havenir_hotel_erpnext.events.sales_invoice.release_all", //dotted path to server method
                    args:{table:frm.doc.table},
                    callback: function(r) {
                        // code snippet

                    }
                })
            }, 'Release Table');

            frm.add_custom_button('Seat', () => {
                new frappe.ui.form.MultiSelectDialog({
                    doctype: "Restaurant Table Seat",
                    target: frm,
                    setters: {
                        status: 'Occupied',
                        party: frm.doc.doctype,
                        party_name: frm.doc.name
                    },
                    action(selections) {
                        selections.forEach((item, i) => {
                            frappe.call({
                                method: "havenir_hotel_erpnext.events.sales_invoice.release_seat", //dotted path to server method
                                args:{seat:item},
                                callback: function(r) {
                                    // code snippet
                                    frappe.msgprint(__(`Seat ${item} released.`));

                                }
                            })
                        });


                    }
                    });
            }, 'Release Table');
        }
	},
    table(frm){
        // update table seats
        // set query filter
        frm.set_query('seat', 'restaurant_table_seat', () => {
            return {
                filters: {
                    table: frm.doc.table
                }
            }
        })
        update_table_seats(frm);
    },
    full_capacity(frm){
        // update table seats
        update_table_seats(frm);
    }
})

frappe.ui.form.on('Restaurant Table Seat Detail', {
	refresh(frm) {
		// your code here
	},
    seat: (frm, cdt, cdn)=>{
        let row = locals[cdt][cdn];
        frm.doc.restaurant_table_seat.forEach((item, i) => {
            if(item.seat==row.seat && item.idx!=row.idx){
                let seat = row.seat;
                row.seat = '';
                frm.refresh_field('restaurant_table_seat');
                frappe.throw(__(`${seat} already exists in row ${item.idx}`));
            }
        });

    }
})



// methods
let update_table_seats = (frm)=>{
        // initialize table
        if (frm.doc.full_capacity) {
            frappe.call({
                method: "havenir_hotel_erpnext.api.doctype.get_tableinvoice_seats", //dotted path to server method
                args:{table:frm.doc.table,
                        party:frm.doc.doctype,
                        party_name:frm.doc.name},
                callback: function(r) {
                    // code snippet
                    if(r.message){
                        let d = r.message;
                        frm.doc.restaurant_table_seat = [];
                        d.forEach((item, i) => {
                            frm.add_child('restaurant_table_seat', {
                                seat:item.name
                            })
                        });
                        frm.refresh_field('restaurant_table_seat');

                    } else {
                        frappe.throw("No seats assigned to table.")
                    }
                }
            })
        } else {
        frm.set_value('full_capacity', '');
        frappe.throw(__("Please select table."));
    }
}
