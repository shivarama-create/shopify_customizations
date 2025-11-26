import frappe
import re
from ecommerce_integrations.shopify import product as shopify_product_module

# Store the original function
original_create_items = shopify_product_module.create_items_if_not_exist

def custom_create_items_if_not_exist(order):
    """
    Enhanced handler for null product_id items:
    - Tips: Skip item creation (pass through to SO)
    - Custom items: Create items via SQL
    - Change requests: Skip (will be handled in SO if needed)
    """
    line_items = order.get("line_items", [])
    
    # Separate items
    items_with_product_id = []
    items_without_product_id = []
    
    for item in line_items:
        product_id = item.get("product_id")
        
        if not product_id:
            items_without_product_id.append(item)
        else:
            items_with_product_id.append(item)
    
    # Handle null product_id items
    for item in items_without_product_id:
        classification = classify_null_item(item)
        
        if classification == 'custom_item':
            # Create item for custom products
            handle_custom_item(item, order)
        # Tips and change requests: skip item creation
    
    # Call ORIGINAL function for items with valid product_id
    if items_with_product_id:
        order_copy = dict(order)
        order_copy["line_items"] = items_with_product_id
        original_create_items(order_copy)

# Apply override
shopify_product_module.create_items_if_not_exist = custom_create_items_if_not_exist

def classify_null_item(line_item):
    """
    Classify null product_id items:
    - 'tip': Tips (skip item creation)
    - 'custom_item': Custom products (create item)
    - 'change_request': Change/modification requests (skip item creation)
    """
    title = (line_item.get('title') or line_item.get('name') or '').lower()
    price = float(line_item.get('price', 0))
    
    # Check for tip
    if 'tip' in title:
        return 'tip'
    
    # Check for change requests
    change_keywords = [
        'change', 'modify', 'update', 'alter', 'adjust',
        'thickness', 'size', 'dimension', 'requirement'
    ]
    
    if any(keyword in title for keyword in change_keywords):
        return 'change_request'
    
    # Check for sample orders (often custom/free items)
    if 'sample order' in title or price == 0:
        return 'custom_item'
    
    # Default to custom_item for safety
    return 'custom_item'

def handle_custom_item(line_item, order):
    """Create Item for custom products using direct SQL"""
    item_name = line_item.get("name") or line_item.get("title") or "Custom Item"
    sku = line_item.get("sku", "")
    
    # Determine item code
    if sku and sku.strip():
        item_code = sku.strip()
    else:
        sanitized = re.sub(r'[^A-Za-z0-9\s-]', '', item_name)
        item_code = f"SHOPIFY-CUSTOM-{sanitized.replace(' ', '-')[:40].upper()}"
    
    # Check if exists
    if frappe.db.exists("Item", item_code):
        frappe.log_error(
            title="Shopify Custom Item Already Exists",
            message=f"Item {item_code} already exists. Skipping creation."
        )
        return item_code
    
    # Get item group
    item_group = "Products"
    if frappe.db.exists("Shopify Settings"):
        try:
            shopify_settings = frappe.get_single("Shopify Settings")
            if hasattr(shopify_settings, "item_group") and shopify_settings.item_group:
                item_group = shopify_settings.item_group
        except:
            pass
    
    price = float(line_item.get("price", 0))
    description = f"Shopify custom item (product_id: null) from order {order.get('name', 'Unknown')}: {item_name}"
    
    # Direct SQL insert to bypass validation
    try:
        frappe.db.sql("""
            INSERT INTO `tabItem` (
                name, item_code, item_name, item_group, stock_uom,
                is_stock_item, is_sales_item, standard_rate, description,
                docstatus, creation, modified, modified_by, owner
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s
            )
        """, (
            item_code, item_code, item_name, item_group, "Nos",
            0, 1, price, description,
            0, "Administrator", "Administrator"
        ))
        
        frappe.db.commit()
        
        # Log success
        log_custom_item(line_item, order, item_code)
        
    except Exception as e:
        # Log error
        frappe.log_error(
            title=f"Shopify Custom Item Creation Failed: {item_code}",
            message=f"Order: {order.get('name')}\nError: {str(e)}"
        )
    
    return item_code

def log_custom_item(line_item, order, item_code):
    """Create audit log for custom item creation"""
    order_id = order.get("id", "Unknown")
    order_name = order.get("name", "Unknown")
    price = line_item.get("price", "0")
    quantity = line_item.get("quantity", "0")
    sku = line_item.get("sku", "N/A")
    line_item_name = line_item.get("name") or line_item.get("title", "Unknown")
    
    frappe.log_error(
        title=f"Shopify Custom Item Created: {item_code}",
        message=f"""
Order: {order_name} (ID: {order_id})
Line Item: {line_item_name}
Item Code Created: {item_code}
Price: {price}
Quantity: {quantity}
SKU: {sku}
Reason: product_id is null (custom item)
        """
    )