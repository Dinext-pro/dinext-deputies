import frappe
from frappe.utils import today


# возвращает список активных заместителей сегодня
@frappe.whitelist()
def get_delegatable_users():
	user = frappe.session.user
	user_roles = frappe.get_roles()

	if "System Manager" in user_roles or user == "Administrator":
		return frappe.get_all(
			"User",
			filters={"enabled": 1},
			fields=["name", "full_name"],
			order_by="full_name asc",
		)

	today_date = today()
	User = frappe.qb.DocType("User")
	UserDelegate = frappe.qb.DocType("User Delegate")

	return (
		frappe.qb.from_(User)
		.inner_join(UserDelegate)
		.on(UserDelegate.delegator == User.name)
		.select(User.name, User.full_name)
		.where(UserDelegate.delegate == user)
		.where(UserDelegate.from_date <= today_date)
		.where(UserDelegate.to_date >= today_date)
		.where(User.enabled == 1)
		.orderby(User.full_name)
		.run(as_dict=True)
	)
