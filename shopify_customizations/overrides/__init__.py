import frappe
import re
from ecommerce_integrations.shopify import product as shopify_product_module

# Store the original function
original_create_items = shopify_product_module.create_items_if_not_exist

def custom_create_items_if_not_exist(order):
    """
    Only handle items with null product_id.
    All other items go through original Shopify connector flow.
    """
    line_items = order.get("line_items", [])
    
    # Separate items into two groups
    items_with_product_id = []
    items_without_product_id = []
    
    for item in line_items:
        product_id = item.get("product_id")
        
        if not product_id:
            # Null product_id - handle separately
            items_without_product_id.append(item)
        else:
            # Valid product_id - keep for original flow
            items_with_product_id.append(item)
    
    # Handle null product_id items (tips, custom items, etc.)
    for item in items_without_product_id:
        handle_misc_line_item(item, order)
    
    # Call ORIGINAL function for items with valid product_id
    # This ensures zero impact on normal flow
    if items_with_product_id:
        # Create temporary order dict with only valid items
        order_copy = dict(order)
        order_copy["line_items"] = items_with_product_id
        
        # Call original function - 100% unchanged behavior
        original_create_items(order_copy)

# Apply override
shopify_product_module.create_items_if_not_exist = custom_create_items_if_not_exist


# ============ HELPER FUNCTIONS ============
def handle_misc_line_item(line_item, order):
    """Create/retrieve Item for tips and custom additions without product_id"""
    item_name = line_item.get("name") or line_item.get("title") or "Custom Item"
    title_lower = item_name.lower()
    is_tip = "tip" in title_lower
    sku = line_item.get("sku", "")
    
    # Determine item code
    if sku and sku.strip():
        # Use SKU if available
        item_code = sku.strip()
    elif is_tip:
        # Simple code for tips
        item_code = "TIP"
    else:
        # Create sanitized item code for other custom items
        sanitized = re.sub(r'[^A-Za-z0-9\s-]', '', item_name)
        item_code = f"SHOPIFY-MISC-{sanitized.replace(' ', '-')[:40].upper()}"
    
    # Check if item already exists
    if frappe.db.exists("Item", item_code):
        frappe.log_error(
            title="Shopify Null Product ID - Item Already Exists",
            message=f"Item {item_code} already exists. Skipping creation."
        )
        return item_code
    
    # Get item group from Shopify Settings
    item_group = "Products"
    if frappe.db.exists("Shopify Settings"):
        shopify_settings = frappe.get_single("Shopify Settings")
        if hasattr(shopify_settings, "item_group") and shopify_settings.item_group:
            item_group = shopify_settings.item_group
    
    # Get price
    price = line_item.get("price", 0)
    if price:
        price = float(price)
    
    # Create new Item
    item_doc = frappe.get_doc({
        "doctype": "Item",
        "item_code": item_code,
        "item_name": item_name,
        "item_group": item_group,
        "stock_uom": "Nos",
        "is_stock_item": 0,  # Non-inventory item
        "is_sales_item": 1,
        "standard_rate": price,
        "description": f"Shopify {'tip' if is_tip else 'custom item'} (no product_id): {item_name}",
    })
    
    # Add Shopify fields if they exist as custom fields
    if hasattr(item_doc, "shopify_product_id"):
        item_doc.shopify_product_id = ""
    if hasattr(item_doc, "shopify_variant_id"):
        item_doc.shopify_variant_id = ""
    
    item_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Log this for tracking
    log_misc_item(line_item, order, item_code, is_tip)
    
    return item_code


def log_misc_item(line_item, order, item_code, is_tip):
    """Create audit log for miscellaneous items"""
    order_id = order.get("id", "Unknown")
    order_name = order.get("name", "Unknown")
    price = line_item.get("price", "0")
    quantity = line_item.get("quantity", "0")
    sku = line_item.get("sku", "N/A")
    line_item_name = line_item.get("name") or line_item.get("title", "Unknown")
    
    frappe.log_error(
        title=f"Shopify {'Tip' if is_tip else 'Custom Item'} Created",
        message=f"""
Order: {order_name} (ID: {order_id})
Line Item: {line_item_name}
Item Code Created: {item_code}
Price: {price}
Quantity: {quantity}
SKU: {sku}
Reason: product_id is null (expected for tips/custom items)
        """
    )
