# Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Agency(Document):
	pass


@frappe.whitelist()
def create_supplier(agency_name , territory ):
	"""Create a Supplier from the Agency"""
	try:
		# Check if supplier already exists
		if frappe.db.exists("Supplier", agency_name):
			frappe.throw(f"Supplier with name '{agency_name}' already exists") # suppose agency name = supplier name
		
		# Create new supplier document
		supplier = frappe.new_doc("Supplier")
		supplier.supplier_name = agency_name
		supplier.supplier_type = "Company"  
		
		# Map additional fields
		if territory:
			supplier.country = territory
		
		# Save the supplier
		supplier.insert()
		
		frappe.msgprint(f"Supplier '{agency_name}' created successfully")
		return supplier.name
		
	except Exception as e:
		frappe.throw(f"Error creating supplier: {str(e)}")