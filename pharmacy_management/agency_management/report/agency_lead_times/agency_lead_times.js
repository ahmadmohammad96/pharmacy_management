// Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
// For license information, please see license.txt

// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["Agency Lead Times"] = {
    "filters": [
        {
            "fieldname": "agency",
            "label": __("Agency"),
            "fieldtype": "Link",
            "options": "Agency"
        },
        {
            "fieldname": "territory",
            "label": __("Territory"),
            "fieldtype": "Link",
            "options": "Territory"
        },
        {
            "fieldname": "is_active",
            "label": __("Active"),
            "fieldtype": "Select",
            "options": "\nYes\nNo",
        }
    ],
    
 
};