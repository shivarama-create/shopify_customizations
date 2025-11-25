import frappe
import re
from ecommerce_integrations.shopify.product import ShopifyProduct
from ecommerce_integrations.shopify import product as shopify_product_module

# ============ OVERRIDE sync_product METHOD ============
original_sync_product = ShopifyProduct.sync_product

def custom_sync_product(self):
    """Override to handle null product_id (tips, custom items, deleted products)"""
    if not self.product_id or str(self.product_id).lower() == 'null':
        frappe.log_error(
            title="Shopify Sync - Null Product ID Skipped",
            message=f"""
                Skipped syncing product with null product_id.
                This is expected for tips, custom items, or deleted products.
                Variant ID: {self.variant_id}
            """
        )
        return None
    
    # Call original method for valid product_ids
    return original_sync_product(self)

# Apply override
ShopifyProduct.sync_product = custom_sync_product


# ============ OVERRIDE create_items_if_not_exist FUNCTION ============
original_create_items = shopify_product_module.create_items_if_not_exist

def custom_create_items_if_not_exist(order):
    """Handle line items with null product_id separately"""
    for item in order.line_items:
        # Handle null product_id (tips, custom items, etc.)
        if not item.product_id:
            handle_misc_line_item(item, order)
            continue
        
        # Normal flow for valid products
        product = ShopifyProduct(item.product_id, item.variant_id)
        if not frappe.db.exists("Item", {"shopify_product_id": item.product_id}):
            product.sync_product()

# Apply override
shopify_product_module.create_items_if_not_exist = custom_create_items_if_not_exist


# ============ HELPER FUNCTIONS ============
def handle_misc_line_item(line_item, order):
    """Create/retrieve Item for tips and custom additions without product_id"""
    item_name = line_item.name or "Custom Item"
    is_tip = "tip" in item_name.lower()
    
    # Create sanitized item code
    sanitized = re.sub(r'[^A-Za-z0-9\s-]', '', item_name)
    item_code = f"SHOPIFY-{'TIP' if is_tip else 'MISC'}-{sanitized.replace(' ', '-')[:40].upper()}"
    
    # Ensure unique item code
    if frappe.db.exists("Item", item_code):
        return item_code
    
    # Get Shopify Settings for item group
    try:
        shopify_settings = frappe.get_single("Shopify Settings")
        item_group = shopify_settings.price_list or "Products"
    except:
        item_group = "Products"
    
    # Create new Item
    item_doc = frappe.get_doc({
        "doctype": "Item",
        "item_code": item_code,
        "item_name": item_name,
        "item_group": item_group,
        "stock_uom": "Nos",
        "is_stock_item": 0,  # Non-inventory item
        "description": f"Shopify {'tip' if is_tip else 'custom item'} (no product_id): {item_name}",
        "shopify_product_id": "",
        "shopify_variant_id": "",
    })
    
    item_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Log this for tracking
    log_misc_item(line_item, order, item_code, is_tip)
    
    return item_code


def log_misc_item(line_item, order, item_code, is_tip):
    """Create audit log for miscellaneous items"""
    try:
        log_content = f"""
            <b>Shopify {'Tip' if is_tip else 'Custom Item'} Created</b><br><br>
            <b>Order:</b> {order.name}<br>
            <b>Line Item:</b> {line_item.name}<br>
            <b>Item Code:</b> {item_code}<br>
            <b>Price:</b> {line_item.price}<br>
            <b>Quantity:</b> {line_item.quantity}<br>
            <b>SKU:</b> {getattr(line_item, 'sku', 'N/A')}<br>
            <b>Reason:</b> product_id is null (expected for tips/custom items)
        """
        
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": "Item",
            "reference_name": item_code,
            "content": log_content
        }).insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.log_error(f"Failed to log misc item: {str(e)}", "Shopify Misc Item Log Error")

