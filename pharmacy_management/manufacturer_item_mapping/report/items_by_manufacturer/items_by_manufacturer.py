# Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
# For license information, please see license.txt

# import frappe


# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """Return columns and data for the Items by Manufacturer report"""
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Define the columns for the report"""
    return [
        {
            "fieldname": "manufacturer",
            "label": _("Manufacturer"),
            "fieldtype": "Link",
            "options": "Manufacturer",
            "width": 200
        },
        {
            "fieldname": "manufacturer_gln",
            "label": _("GLN"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "is_blocked",
            "label": _("Blocked"),
            "fieldtype": "Check",
            "width": 80
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "part_number",
            "label": _("Part Number"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "gtin",
            "label": _("GTIN"),
            "fieldtype": "Data",
            "width": 140
        },
        {
            "fieldname": "item_group",
            "label": _("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 120
        }
    ]


def get_data(filters=None):
    """Get the data for the report using ORM"""
    data = []
    
    # Build filters for manufacturers
    manufacturer_filters = {}
    
    if filters:
        if filters.get("manufacturer"):
            manufacturer_filters["name"] = filters.get("manufacturer")
        if filters.get("is_blocked") == "Yes":
            manufacturer_filters["is_blocked"] = 1
        elif filters.get("is_blocked") == "No":
            manufacturer_filters["is_blocked"] = 0
    
    # Get manufacturers using ORM
    manufacturers = frappe.get_all(
        "Custom Manufacturer",
        filters=manufacturer_filters,
        fields=["name", "manufacturer_name", "gln", "is_blocked"],
        order_by="manufacturer_name"
    )
    
    # For each manufacturer, get its item mappings
    for manufacturer in manufacturers:
        
        # Build filters for manufacturer items
        item_filters = {"manufacturer": manufacturer.name}
        if filters and filters.get("item_code"):
            item_filters["item_code"] = filters.get("item_code")
        
        # Get manufacturer items using ORM
        manufacturer_items = frappe.get_all(
            "Custom Manufacturer Item",
            filters=item_filters,
            fields=["item_code", "part_number", "gtin"],
            order_by="item_code"
        )
        
        if manufacturer_items:
            # Manufacturer has items - show each item
            for item in manufacturer_items:
                # Get item details
                item_doc = frappe.get_doc("Item", item.item_code)
                
                data.append({
                    "manufacturer": manufacturer.name,
                    "manufacturer_gln": manufacturer.gln,
                    "is_blocked": manufacturer.is_blocked,
                    "item_code": item.item_code,
                    "item_name": item_doc.item_name,
                    "part_number": item.part_number,
                    "gtin": item.gtin,
                    "item_group": item_doc.item_group
                })
        else:
            # Manufacturer has no items - show manufacturer with empty item fields
            data.append({
                "manufacturer": manufacturer.name,
                "manufacturer_gln": manufacturer.gln,
                "is_blocked": manufacturer.is_blocked,
                "item_code": None,
                "item_name": None,
                "part_number": None,
                "gtin": None,
                "item_group": None
            })
    
    return data


