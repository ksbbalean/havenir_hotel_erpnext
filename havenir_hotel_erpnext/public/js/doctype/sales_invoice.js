frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// filter restaurant table
		set_table_filter(frm);
		// your code here
	},
	split_bill_by(frm) {
		if(frm.doc.split_bill_by && (frm.doc.items.length>0)){
			if(frm.doc.split_bill_by=='Table' && frm.doc.restaurant_tables.length>0){
				frm.set_value('bill_per_table', frm.doc.grand_total/frm.doc.restaurant_tables.length);
			} else if(frm.doc.split_bill_by!='Table'){

			} else {
				frappe.throw(__("Please select restaurant tables first."));
				frm.set_value('bill_per_table', 0.00);
			}
		} else {
			frm.set_value('bill_per_table', '');
			frappe.throw(__("Please select items first."));
		}
	},
	how_many_individuals(frm){
		if(frm.doc.how_many_individuals>0){
			frm.set_value('bill_per_individual', frm.doc.grand_total/frm.doc.how_many_individuals);
		} else {
			frm.set_value('bill_per_individual', 0.00);
		}
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
		calculate_table_bill(frm);
    },
	restaurant_tables_remove: (frm, cdt, cdn)=>{
		calculate_table_bill(frm);
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


let calculate_table_bill = (frm)=>{
	if(frm.doc.split_bill_by=='Table'){
		if(frm.doc.restaurant_tables.length>0){
			frm.set_value('bill_per_table', frm.doc.grand_total/frm.doc.restaurant_tables.length);
		} else {
			frm.set_value('bill_per_table', 0.00);
		}
	}
}
