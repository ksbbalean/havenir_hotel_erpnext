import frappe
from erpnext.manufacturing.doctype.work_order.work_order import (
    make_stock_entry
)


def on_update(doc, event):
    # work order update event
    if(doc.workflow_state=="Completed"):
        # make stock entry
        _make = make_stock_entry(doc.name, 'Manufacture', doc.qty)
        se = frappe.get_doc(_make)
        se.insert(ignore_permissions=True)
        se.submit()


# @frappe.whitelist()
# def make_manufacture(doc):
#     stock_entry = frappe.new_doc('Stock Entry')
#     stock_entry.stock_entry_type = 'Manufacture'
#     stock_entry.work_order = doc.name
#     stock_entry.from_bom = True
#     stock_entry.fg_completed_qty = doc.qty
#     stock_entry.use_multi_level_bom = True
#     stock_entry.bom_no = doc.bom_no
#     stock_entry.from_warehouse = 'Kitchen In Progress - E'
#     stock_entry.to_warehouse = 'Kitchen In Progress - E'
#     # get items
#     for item in doc.required_items:
#         se_child = stock_entry.append('items')
#         se_child.s_warehouse = 'Kitchen In Progress - E'
#         se_child.item_code = item.item_code
#         se_child.item_name = item.item_name
#         se_child.description = item.description
#         se_child.qty = item.required_qty
#         se_child.qty = item.rate
#         se_child.basic_rate = item.rate
#         se_child.expense_account = 'Stock Adjustment - E'
#         se_child.cost_center = 'Main - E'
#     stock_entry.submit()
#     return stock_entry
