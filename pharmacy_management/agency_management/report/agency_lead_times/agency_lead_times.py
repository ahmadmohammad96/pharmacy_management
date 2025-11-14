# Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
# For license information, please see license.txt

# import frappe


# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """Return columns and data for the Agency Lead Times report"""
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Define the columns for the report"""
    return [
        {
            "fieldname": "agency",
            "label": _("Agency"),
            "fieldtype": "Link",
            "options": "Agency",
            "width": 200
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "min_order_qty",
            "label": _("Min Order Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "lead_time_days",
            "label": _("Lead Time (Days)"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "territory",
            "label": _("Territory"),
            "fieldtype": "Link",
            "options": "Territory",
            "width": 120
        },
        {
            "fieldname": "is_active",
            "label": _("Active"),
            "fieldtype": "Check",
            "width": 80
        }
    ]


def get_data(filters=None):
    """Get the data for the report using ORM"""
    data = []
    
    # Build filters for frappe.get_all
    agency_filters = {}
    
    if filters:
        if filters.get("agency"):
            agency_filters["name"] = filters.get("agency")
        if filters.get("territory"):
            agency_filters["territory"] = filters.get("territory")
        if filters.get("is_active") == "Yes":
            agency_filters["is_active"] = 1
        elif filters.get("is_active") == "No":
            agency_filters["is_active"] = 0
    
    # Get agencies using ORM
    agencies = frappe.get_all(
        "Agency",
        filters=agency_filters,
        fields=["name", "territory", "is_active"],
        order_by="name"
    )
    
    # For each agency, get its items
    for agency in agencies:
        agency_doc = frappe.get_doc("Agency", agency.name)
        
        if agency_doc.items:
            # Agency has items - show each item
            for item in agency_doc.items:
                data.append({
                    "agency": agency.name,
                    "item_code": item.item_code,
                    "min_order_qty": item.min_order_qty,
                    "lead_time_days": item.lead_time_days,
                    "territory": agency.territory,
                    "is_active": agency.is_active
                })
        else:
            # Agency has no items - show agency with empty item fields
            data.append({
                "agency": agency.name,
                "item_code": None,
                "min_order_qty": None,
                "lead_time_days": None,
                "territory": agency.territory,
                "is_active": agency.is_active
            })
    
    return data


