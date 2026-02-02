import frappe
from frappe import _
from frappe.utils import getdate, today

#возвращает список активных заместителей сегодня
@frappe.whitelist()
def get_delegatable_users():
    user = frappe.session.user
     # Получить роли текущего пользователя  
    user_roles = frappe.get_roles()  
  
    # Проверить наличие роли  
    if "System Manager" in user_roles or user == "Administrator":
        return frappe.get_all("User", filters={"enabled": 1}, fields=["name", "full_name"])

    from frappe.utils import today
    today_date = today()

    return frappe.db.sql("""
        SELECT u.name, u.full_name
        FROM `tabUser` u
        INNER JOIN `tabUser Delegate` d ON d.delegator = u.name
        WHERE d.delegate = %s
          AND d.from_date <= %s
          AND d.to_date >= %s
          AND u.enabled = 1
    """, (user, today_date, today_date), as_dict=True)