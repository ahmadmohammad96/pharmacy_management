## Pharmacy Management

pharmacy_management

#### License

mit

## HOW TO SETUP
- bench get-app 
- bench --site your_site install-app pharmacy_management
- bench --site your_site migrate


## HOW TO TEST 

I followed the instructions of the needed requirements in PDF , implemented them and followed the best practice when possible 
You will also find some "" additional validation "" when you test it by hand , here I will write the summarized description 

## Module 1
TEST for : Prevent deactivating an Agency if it has linked items.
- got to Agency --> test 1 agency and try to uncheck "Is Active" ,, this will raise exception

TEST for : Button “Create Supplier”: generates a Supplier from the Agency
- got to got to Agency --> test 1 agency for example and press : Actions : Create Supplier
- then go to Supplier and check for the new created supplier 

TEST for : Inactive Agencies show in red on list view.
- go to Agency List view and check the colors , code is in client script 

TEST for : Report: Agency Lead Times (Agency, Item, Min Order Qty, Lead Time).
- got to Report --> Agency Lead Times : Show Report (I added some basic filters)


## Module 2
## Since there are core doctypes called Manufacturer and Manufacturer Item -- I named the new one as Custome Manufacturer and Custom Manufacturer Item

TEST for : Block adding Manufacturer Items if Manufacturer is marked as blocked.
- Go to Custom Manufacturer  --> try to check the Is Blocked checkbox 
- Now go to : Custom Manufacturer Item --> try to create a new document and select the previous Custom Manufacturer document , it will raise exception , then uncheck the box and retry to create the document 

TEST for : Ensure (manufacturer, item_code) pair is unique.
- Try to create another new document that has the same Manufacturer and same item code of another Custom Manufacturer Item 

TEST for : Auto-fill part_number with item_code if left blank.
- try to create a Custom Manufacturer Item with leaving part_number empty and save , it will be auto fill with item code 

TEST for : REST API: return all manufacturer mappings for a given item_code.
try to make a simple GET with this simple JS code , press f12 in yourkeyboard and paste this : 

frappe.call({
    method: 'pharmacy_management.manufacturer_item_mapping.doctype.custom_manufacturer_item.custom_manufacturer_item.get_manufacturer_mappings_for_item',
    args: {
        item_code: 'test 1 item'  // Use an item from your fixtures
    },
    callback: function(r) {
        console.log('API Response:', r.message);
    }
});

TEST for : Report: Items by Manufacturer
- Go to Report -->Items by Manufacturer : Show Report

## AI Usage Log is in AI_logs.txt