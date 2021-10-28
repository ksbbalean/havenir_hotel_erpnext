// Copyright (c) 2020, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Restaurant Tables', {
	refresh: function(frm) {
        // release table buttons
        // Custom buttons in groups
        frm.add_custom_button('All Seats', () => {
            frm.call('release_all');
        }, 'Release Table');

        frm.add_custom_button('Seat', () => {
            new frappe.ui.form.MultiSelectDialog({
                doctype: "Restaurant Table Seat",
                target: frm,
                setters: {
                    table: frm.doc.name,
                    status: 'Occupied'
                },
                action(selections) {
                    selections.forEach((item, i) => {
                        frm.call('release_seat', {seat:item});
                    });
                    frappe.msgprint(__("Seat(s) released."));

                }
                });
        }, 'Release Table');

	}
});

frappe.ui.form.on('Restaurant Table Seat Detail', {
	// refresh: function(frm) {

	// },
    seat: (frm, cdt, cdn)=>{
        let row = locals[cdt][cdn];
        frm.doc.seats.forEach((item, i) => {
            if(item.seat==row.seat && item.idx!=row.idx){
                let seat = row.seat;
                row.seat = '';
                frm.refresh_field('seats');
                frappe.throw(__(`${seat} already exists in row ${item.idx}`));
            }
        });

    }

});
