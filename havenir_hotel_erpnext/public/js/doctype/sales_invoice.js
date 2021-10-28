frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// your code here
	},
    table(frm){
        // update table seats
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
	}
})



// methods
let update_table_seats = (frm)=>{
    if(frm.doc.table){
        // initialize table
        if (frm.doc.full_capacity) {
            frappe.call({
                method: "havenir_hotel_erpnext.api.doctype.get_table_seats", //dotted path to server method
                args:{table:frm.doc.table},
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
        }
    } else {
        frm.set_value('full_capacity', '');
        frappe.throw(__("Please select table."));
    }
}
