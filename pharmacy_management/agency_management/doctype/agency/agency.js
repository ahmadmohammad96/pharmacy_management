// Copyright (c) 2025, ahmad900mohammad@gmail.com and contributors
// For license information, please see license.txt

// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Agency', {
    refresh: function(frm) {
        // Add Create Supplier button
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('Create Supplier'), function() {
                frappe.call({
                    method: "pharmacy_management.agency_management.doctype.agency.agency.create_supplier",
                    args : { agency_name : frm.doc.name, territory : frm.doc.territory},
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Supplier created successfully: {0}', [r.message]));
                        }
                    }
                });
            }, __('Actions'));
        }
    },
    
    before_save: function(frm) {
        // Validate before deactivating
        if (!frm.doc.is_active && frm.doc.items && frm.doc.items.length > 0) {
            frappe.throw(__('Cannot deactivate Agency as it has linked items'));
        }
    }
});