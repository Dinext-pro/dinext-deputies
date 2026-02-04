import frappe
from frappe import _
from frappe.utils import today
from frappe.model.document import Document

class UserDelegate(Document):
	pass

# Проверяет, может ли текущий пользователь (frappe.session.user)
# замещать указанного пользователя `user` в текущий день.
@frappe.whitelist()
def can_impersonate_as(user: str) -> bool:

    current_user = frappe.session.user
    user_roles = frappe.get_roles()  

    if current_user == "Administrator" or "System Manager" in user_roles:
        return True

    today_date = today()
    count = frappe.db.count("User Delegate", {
        "delegate": current_user,
        "delegator": user,
        "from_date": ["<=", today_date],
        "to_date": [">=", today_date]
    })
    return count > 0