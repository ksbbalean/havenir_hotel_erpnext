frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// filter restaurant table
		set_table_filter(frm);
		// your code here
        // if(!frm.is_new()){
        //     frm.add_custom_button('All Seats', () => {
        //         frappe.call({
        //             method: "havenir_hotel_erpnext.events.sales_invoice.release_all", //dotted path to server method
        //             args:{table:frm.doc.table},
        //             callback: function(r) {
        //                 // code snippet
		//
        //             }
        //         })
        //     }, 'Release Table');
		//
        //     frm.add_custom_button('Seat', () => {
        //         new frappe.ui.form.MultiSelectDialog({
        //             doctype: "Restaurant Table Seat",
        //             target: frm,
        //             setters: {
        //                 status: 'Occupied',
        //                 party: frm.doc.doctype,
        //                 party_name: frm.doc.name
        //             },
        //             action(selections) {
        //                 selections.forEach((item, i) => {
        //                     frappe.call({
        //                         method: "havenir_hotel_erpnext.events.sales_invoice.release_seat", //dotted path to server method
        //                         args:{seat:item},
        //                         callback: function(r) {
        //                             // code snippet
        //                             frappe.msgprint(__(`Seat ${item} released.`));
		//
        //                         }
        //                     })
        //                 });
		//
		//
        //             }
        //             });
        //     }, 'Release Table');
        // }

	}
})

frappe.ui.form.on('SI Restaurant Table Detail', {
	refresh(frm) {
		// your code here
	},
    table: (frm, cdt, cdn)=>{
        let row = locals[cdt][cdn];
        frm.doc.restaurant_tables.forEach((item, i) => {
            if(item.table==row.table && item.idx!=row.idx){
                let table = row.table;
                row.table = '';
				row.capacity = '';
                frm.refresh_field('restaurant_tables');
                frappe.throw(__(`${table} already exists in row ${item.idx}`));
            }
        });

    }
})


let set_table_filter = (frm)=>{
	frm.set_query('table', 'restaurant_tables', () => {
		return {
			query: 'havenir_hotel_erpnext.api.doctype.setsi_table_filter',
			filters: {
				occupied: false,
				docname: frm.doc.name,
				doctype: frm.doc.doctype
			}
		}
	})
}


// methods
// let update_table_seats = (frm)=>{
//         // initialize table
//         if (frm.doc.full_capacity) {
//             frappe.call({
//                 method: "havenir_hotel_erpnext.api.doctype.get_tableinvoice_seats", //dotted path to server method
//                 args:{table:frm.doc.table,
//                         party:frm.doc.doctype,
//                         party_name:frm.doc.name},
//                 callback: function(r) {
//                     // code snippet
//                     if(r.message){
//                         let d = r.message;
//                         frm.doc.restaurant_table_seat = [];
//                         d.forEach((item, i) => {
//                             frm.add_child('restaurant_table_seat', {
//                                 seat:item.name
//                             })
//                         });
//                         frm.refresh_field('restaurant_table_seat');
//
//                     } else {
//                         frappe.throw("No seats assigned to table.")
//                     }
//                 }
//             })
//         } else {
//         frm.set_value('full_capacity', '');
//         frappe.throw(__("Please select table."));
//     }
// }
