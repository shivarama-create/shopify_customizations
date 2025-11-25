app_name = "shopify_customizations"
app_title = "Shopify Customizations"
app_publisher = "Your Company"
app_description = "Custom overrides for Shopify integration"
app_version = "0.0.1
app_email = "shivarama@cozycornerpatios.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "shopify_customizations",
# 		"logo": "/assets/shopify_customizations/logo.png",
# 		"title": "Shopify Customizations",
# 		"route": "/shopify_customizations",
# 		"has_permission": "shopify_customizations.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shopify_customizations/css/shopify_customizations.css"
# app_include_js = "/assets/shopify_customizations/js/shopify_customizations.js"

# include js, css files in header of web template
# web_include_css = "/assets/shopify_customizations/css/shopify_customizations.css"
# web_include_js = "/assets/shopify_customizations/js/shopify_customizations.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shopify_customizations/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "shopify_customizations/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "shopify_customizations.utils.jinja_methods",
# 	"filters": "shopify_customizations.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "shopify_customizations.install.before_install"
# after_install = "shopify_customizations.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "shopify_customizations.uninstall.before_uninstall"
# after_uninstall = "shopify_customizations.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "shopify_customizations.utils.before_app_install"
# after_app_install = "shopify_customizations.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "shopify_customizations.utils.before_app_uninstall"
# after_app_uninstall = "shopify_customizations.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shopify_customizations.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"shopify_customizations.tasks.all"
# 	],
# 	"daily": [
# 		"shopify_customizations.tasks.daily"
# 	],
# 	"hourly": [
# 		"shopify_customizations.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shopify_customizations.tasks.weekly"
# 	],
# 	"monthly": [
# 		"shopify_customizations.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "shopify_customizations.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "shopify_customizations.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shopify_customizations.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "shopify_customizations.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["shopify_customizations.utils.before_request"]
# after_request = ["shopify_customizations.utils.after_request"]

# Job Events
# ----------
# before_job = ["shopify_customizations.utils.before_job"]
# after_job = ["shopify_customizations.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"shopify_customizations.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Load Shopify overrides on app startup
after_migrate = "shopify_customizations.overrides"
boot_session = "shopify_customizations.boot.boot_session"

