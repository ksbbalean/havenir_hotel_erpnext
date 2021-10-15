import frappe


def on_update(doc, event):
    # work order update event
    if(doc.workflow_state=="Completed"):
        # make stock entry
        @frappe.whitelist()
        def make_material_receipt(doc):
        	stock_entry = frappe.new_doc('Stock Entry')
        	stock_entry.stock_entry_type = 'Manufacture'
            stock_entry.work_order = doc.name
        	# stock_entry.to_warehouse = self.pms_tank
        	stock_entry.company = self.company
        	expense_account = '' #get_account(None, 'expense_account', 'Healthcare Settings', self.company)
        	# get items
        	for i in self.items:
        		if(i.additional_pms):
        			item = frappe.get_doc('Item', self.item)
        			se_child = stock_entry.append('items')
        			se_child.item_code = item.item_code
        			se_child.item_name = item.item_name
        			se_child.basic_rate = batch.rate
        			# se_child.uom = item.stock_uom
        			se_child.stock_uom = item.stock_uom
        			se_child.qty = flt(i.additional_pms)
        			se_child.t_warehouse = i.tank
        			se_child.batch_no = self.batch
        			# in stock uom
        			# se_child.transfer_qty = flt(self.addit)
        			# se_child.conversion_factor = flt(item.conversion_factor)
        			cost_center = self.cost_center #frappe.get_cached_value('Company',  self.company,  'cost_center')
        			se_child.cost_center = self.cost_center
        			# se_child.expense_account = expense_account

        	if(self.additional_costs):
        		# additional_costs = self.additional_costs
        		additional_costs = []
        		for i in self.additional_costs:
        			newi = i.as_dict()
        			del newi['name']
        			del newi['idx']
        			additional_costs.append(newi)
        			stock_entry.append('additional_costs',
        		 	newi)

        	if submit:
        		stock_entry.submit()
        		# update stock on pms overage
        		self.db_set('stock_entry', stock_entry.name)
        		return stock_entry
        	return stock_entry.as_dict()
