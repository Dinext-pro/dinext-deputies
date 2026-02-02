import frappe
from frappe import _
from frappe.utils import today
from dinext_deputies.dinext_deputies.doctype.user_delegate import can_impersonate_as

@frappe.whitelist(methods=["POST"])
def impersonate_with_delegate(user: str, reason: str):
    current_user = frappe.session.user

    # проверяем права
    if not can_impersonate_as(user):
        frappe.throw(
            _("You are not allowed to impersonate as {0}").format(user),
            frappe.PermissionError
        )

    # логируем действие
    frappe.get_doc({
        "doctype": "Activity Log",
        "user": user,
        "status": "Success",
        "subject": _("User {0} impersonated as {1}").format(current_user, user),
        "operation": "Impersonate",
    }).insert(ignore_permissions=True, ignore_links=True)

    # уведомляем замещаемого
    notification = frappe.new_doc("Notification Log")
    notification.for_user = user
    notification.from_user = current_user
    notification.subject = _("{0} just impersonated as you. Reason: {1}").format(current_user, reason)
    notification.type = "Alert"
    notification.insert(ignore_permissions=True)

    frappe.local.login_manager.impersonate(user)
