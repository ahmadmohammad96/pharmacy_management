// Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
// For license information, please see license.txt

// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["Items by Manufacturer"] = {
    "filters": [
        {
            "fieldname": "manufacturer",
            "label": __("Manufacturer"),
            "fieldtype": "Link",
            "options": "Manufacturer"
        },
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "is_blocked",
            "label": __("Blocked"),
            "fieldtype": "Select",
            "options": "\nYes\nNo"
        }
    ],
    
   
};