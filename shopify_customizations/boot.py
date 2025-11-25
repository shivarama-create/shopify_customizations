import frappe

def boot_session(bootinfo):
    """Load overrides on session start"""
    # Import overrides to apply monkey patches
    from shopify_customizations.overrides import custom_create_items_if_not_exist
