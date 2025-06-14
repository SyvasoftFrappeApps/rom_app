import frappe

app_name = "rom_app"
app_title = "Restaurant Ops Mgmt"
app_publisher = "Pubs"
app_description = "Description"
app_email = "email@email.com"
app_license = "mit"
# required_apps = []


fixtures = [
    {
        "dt": "Role",
        "filters": [
            [
                "name", "in", [
                    "Rom_FB_Role",
                    "Rom_Op_Role",
                    "Rom_Cash_Role",
                    "Rom_Store_Role",
                    "Rom_Manage_Role",
                    "Rom_Admin_Role",
                    "Rom_Dev_Role",
                    "Rom_MasterData_Role",
                    "Rom_HR_Role",
                    "Rom_Sample_Role",
                ]
            ]
        ]
    },
    {
        "dt": "Custom DocPerm",
        "filters": [
            [
                "role", "in", [
                    "Rom_FB_Role",
                    "Rom_Op_Role",
                    "Rom_Cash_Role",
                    "Rom_Store_Role",
                    "Rom_Manage_Role",
                    "Rom_Admin_Role",
                    "Rom_Dev_Role",
                    "Rom_MasterData_Role",
                    "Rom_HR_Role",
                    "Rom_Sample_Role",
                ]
            ]
        ]
    },
    {
        "dt": "Custom Role",
        "or_filters": {
                        "page": ["in",  [
                            "single-page-chart",
                            "inventory-view",
                            "checklist_matrix",
                            "fb-open-check-mob",
                            "fb-close-check-mob",
                            "op-open-check-mob",
                            "op-close-check-mob",
                            "sample-page",
                            ]],
                        "report": ["in", [
                            "FB Opening Checklist Register",
                            "FB Closing Checklist Register",
                            "Chef Indent By Dept Register",
                            "Chef Production Register",
                            "Op Opening Checklist Register",
                            "Op Closing Checklist Register",
                            "Incident Report Register",
                            "Discount Form Register",
                            "Asset Count Register",
                            "Sales Report Register",
                            "Expense Report Register",
                            "Breakages Report Register",
                            "Ticket Report Register",
                            "NC Report Register",
                            "Raw Material Only Register",
                            "Stock Entry Register",
                            "Inventory Wastage Register",
                            "Inventory Counting Register",
                            "Inventory Summary Register",
                            "Inventory Transaction Register",
                            "Asset Master Register",
                            "Menu Register",
                            "SampleDoc Register",
                        ]],
                     }
    },
    {
        "dt": "Translation"
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
                   "/assets/rom_app/css/billboard.css",
                   "/assets/rom_app/css/frappe-datatable.min.css"
                   ]
app_include_js = [
                  "/assets/rom_app/js/d3.v6.min.js",
                  "/assets/rom_app/js/billboard.js",
                  "/assets/rom_app/js/utils_link_formatters.js",
                  "/assets/rom_app/js/frappe-datatable.min.js",
                  "/assets/rom_app/js/Sortable.min.js",
                  ]
# "/assets/rom_app/js/clusterize.js",
# include js, css files in header of web template
# web_include_css = "/assets/rom_app/css/rom_app.css"
# web_include_js = "/assets/rom_app/js/rom_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rom_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"Chef Opening Checklist": "public/js/chef_opening_checklist_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "rom_app/public/icons.svg"

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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "rom_app.utils.jinja_methods",
# 	"filters": "rom_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rom_app.install.before_install"
# after_install = "rom_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rom_app.uninstall.before_uninstall"
# after_uninstall = "rom_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "rom_app.utils.before_app_install"
# after_app_install = "rom_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "rom_app.utils.before_app_uninstall"
# after_app_uninstall = "rom_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rom_app.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
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
# scheduler_events = {}
scheduler_events = {
    "cron": {
        # "58 23 * * *": ["rom_app.scheduled_tasks.call_inventory_summary_night"],
        # "1 0 * * *": ["rom_app.scheduled_tasks.call_inventory_summary_morning"],
        "0 3 * * *": ["rom_app.scheduled_tasks.call_inventory_summary_morning_60_days_before"],
        "5 3 * * *": ["rom_app.scheduled_tasks.call_inventory_summary_morning_for_today_with_one_time_db_write"],
         "0 4 * * *": ["rom_app.scheduled_tasks.generate_raw_material_summary"]
    }
    }
# "58 23 * * *": ["rom_app.scheduled_tasks.inventory_summary"],
# Testing
# -------

# before_tests = "rom_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rom_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "rom_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rom_app.utils.before_request"]
# after_request = ["rom_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["rom_app.utils.before_job"]
# after_job = ["rom_app.utils.after_job"]

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
# 	"rom_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doc_events = {
    "Chef Production": {
        "before_save": "rom_app.restaurant_ops_mgmt.doctype.chef_production.chef_production.update_totals"
    },
    "Stock Entry":{
        "before_save": "rom_app.restaurant_ops_mgmt.doctype.stock_entry.stock_entry.update_totals"
    }
}
