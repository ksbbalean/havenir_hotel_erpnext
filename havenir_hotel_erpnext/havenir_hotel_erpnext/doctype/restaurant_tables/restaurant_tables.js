// Copyright (c) 2020, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Restaurant Tables', {
	// refresh: function(frm) {

	// }
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
