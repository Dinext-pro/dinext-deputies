app_name = "dinext_deputies"
app_title = "Dinext Deputies"
app_publisher = "Dinext"
app_description = "Managing Deputies"
app_email = "info@dinext.ru"
app_license = "mit"

standard_navbar_items = [  
    {  
        "item_label": "Мои замещения",  
        "item_type": "Route",  
        "route": "/app/user-delegate",  
        "is_standard": 1
    }  
]

fixtures = [
    {
        "doctype": "Server Script",
        "filters": [
            ["module", "in", ["Dinext Deputies"]],
            ["disabled", "=", 0]
        ]
    },
    {
        "doctype": "Client Script",
        "filters": [
            ["module", "in", ["Dinext Deputies"]],
            ["enabled", "=", 1]
        ]
    },
    {
        "doctype": "DocType Permission",
        "filters": [
            ["ref_doctype", "in", ["User Delegate"]]
        ]
    }
]

# Apps
# ------------------

required_apps = ["https://github.com/kittiu/doctype_permission.git", "https://dinord.gitlab.yandexcloud.net/erpnext/dinext/dinext_projects.git"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dinext_deputies",
# 		"logo": "/assets/dinext_deputies/logo.png",
# 		"title": "Dinext Deputies",
# 		"route": "/dinext_deputies",
# 		"has_permission": "dinext_deputies.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dinext_deputies/css/dinext_deputies.css"
# app_include_js = "/assets/dinext_deputies/js/dinext_deputies.js"
app_include_js = "/assets/dinext_deputies/js/delegate-impersonate.js"

# include js, css files in header of web template
# web_include_css = "/assets/dinext_deputies/css/dinext_deputies.css"
# web_include_js = "/assets/dinext_deputies/js/dinext_deputies.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dinext_deputies/public/scss/website"

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
# app_include_icons = "dinext_deputies/public/icons.svg"

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
# 	"methods": "dinext_deputies.utils.jinja_methods",
# 	"filters": "dinext_deputies.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dinext_deputies.install.before_install"
# after_install = "dinext_deputies.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dinext_deputies.uninstall.before_uninstall"
# after_uninstall = "dinext_deputies.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dinext_deputies.utils.before_app_install"
# after_app_install = "dinext_deputies.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dinext_deputies.utils.before_app_uninstall"
# after_app_uninstall = "dinext_deputies.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dinext_deputies.notifications.get_notification_config"

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

# scheduler_events = {
# 	"all": [
# 		"dinext_deputies.tasks.all"
# 	],
# 	"daily": [
# 		"dinext_deputies.tasks.daily"
# 	],
# 	"hourly": [
# 		"dinext_deputies.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dinext_deputies.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dinext_deputies.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dinext_deputies.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.core.doctype.user.user.impersonate": "dinext_deputies.overrides.user.impersonate_with_delegate"
}
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dinext_deputies.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dinext_deputies.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dinext_deputies.utils.before_request"]
# after_request = ["dinext_deputies.utils.after_request"]

# Job Events
# ----------
# before_job = ["dinext_deputies.utils.before_job"]
# after_job = ["dinext_deputies.utils.after_job"]

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
# 	"dinext_deputies.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

