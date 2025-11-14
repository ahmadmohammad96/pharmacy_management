# Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomManufacturerItem(Document):
	def validate(self):
		"""Validate Manufacturer Item before saving"""
		if self.manufacturer:
			manufacturer_check = frappe.db.get_value("Custom Manufacturer" , {'manufacturer_name' : self.manufacturer } , ['is_blocked'])
			if manufacturer_check:
				frappe.throw(f"Cannot add items for blocked manufacturer: {self.manufacturer}")


		self.validate_unique_manufacturer_item_pair()
		self.auto_fill_part_number()
		
	def validate_unique_manufacturer_item_pair(self):
		"""Ensure (manufacturer, item_code) pair is unique"""
		if self.manufacturer and self.item_code:
			# Check for existing records with same manufacturer and item_code
			existing = frappe.get_all(
				"Custom Manufacturer Item",
				filters={
					"manufacturer": self.manufacturer,
					"item_code": self.item_code,
					"name": ["!=", self.name]  # Exclude current document for updates
				},
				limit=1
			)
			
			if existing:
				frappe.throw(f"Manufacturer-Item mapping already exists for {self.manufacturer} - {self.item_code}")


	def auto_fill_part_number(self):
		"""Auto-fill part_number with item_code if left blank"""
		if not self.part_number and self.item_code:
			self.part_number = self.item_code



@frappe.whitelist()
def get_manufacturer_mappings_for_item(item_code):
	"""
	REST API endpoint: Return all manufacturer mappings for a given item_code
	Usage: GET /api/method/pharmacy_management.manufacturer_item_mapping.doctype.custom_manufacturer_item.custom_manufacturer_item.get_manufacturer_mappings_for_item?item_code=ITEM001
	"""
	if not item_code:
		frappe.throw("Item code is required")
	
	# Verify item exists
	if not frappe.db.exists("Item", item_code):
		frappe.throw(f"Item {item_code} does not exist")
	
	# Get all manufacturer mappings for the item using ORM
	mappings = frappe.get_all(
		"Custom Manufacturer Item",
		filters={"item_code": item_code},
		fields=[
			"name",
			"manufacturer", 
			"item_code",
			"part_number",
			"gtin",
			"creation",
			"modified"
		],
		order_by="manufacturer"
	)
	
	for mapping in mappings:
		if mapping.manufacturer:
			manufacturer_doc = frappe.get_doc("Custom Manufacturer", mapping.manufacturer)
			mapping.manufacturer_details = {
				"manufacturer_name": manufacturer_doc.manufacturer_name,
				"gln": manufacturer_doc.gln,
				"is_blocked": manufacturer_doc.is_blocked
			}
	
	return {
		"success": True,
		"item_code": item_code,
		"total_mappings": len(mappings),
		"mappings": mappings
	}
