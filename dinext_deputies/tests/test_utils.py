import unittest

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today

TEST_EMAIL_PREFIX = "test_deputies_"
TEST_EMAIL_DOMAIN = "@example.com"


def test_email(label: str) -> str:
	return f"{TEST_EMAIL_PREFIX}{label}{TEST_EMAIL_DOMAIN}"


def create_test_user(email: str, roles=(), enabled: int = 1):
	if frappe.db.exists("User", email):
		user = frappe.get_doc("User", email)
		user.enabled = enabled
		user.save(ignore_permissions=True)
	else:
		user = frappe.new_doc("User")
		user.email = email
		user.first_name = email.split("@", 1)[0]
		user.enabled = enabled
		user.insert(ignore_permissions=True)

	if roles:
		user.add_roles(*roles)

	return user


def create_user_delegate(delegate: str, delegator: str, from_date: str, to_date: str) -> str:
	doc = frappe.get_doc(
		{
			"doctype": "User Delegate",
			"delegate": delegate,
			"delegator": delegator,
			"from_date": from_date,
			"to_date": to_date,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def assert_sorted_by_full_name(test_case: unittest.TestCase, rows: list[dict]):
	test_case.assertTrue(rows, msg="expected non-empty result")
	full_names = [row.get("full_name") or "" for row in rows]
	expected = sorted(full_names, key=lambda value: value.casefold())
	test_case.assertEqual(full_names, expected)


def assert_user_fields(test_case: unittest.TestCase, row: dict):
	test_case.assertIn("name", row)
	test_case.assertIn("full_name", row)


def cleanup_test_deputies_data():
	frappe.db.delete(
		"User Delegate",
		{
			"delegate": ["like", f"{TEST_EMAIL_PREFIX}%{TEST_EMAIL_DOMAIN}"],
		},
	)
	frappe.db.delete(
		"User Delegate",
		{
			"delegator": ["like", f"{TEST_EMAIL_PREFIX}%{TEST_EMAIL_DOMAIN}"],
		},
	)
	frappe.db.delete("User", {"name": ["like", f"{TEST_EMAIL_PREFIX}%{TEST_EMAIL_DOMAIN}"]})


class DeputiesTestCase(FrappeTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		cleanup_test_deputies_data()

	def tearDown(self):
		cleanup_test_deputies_data()
		frappe.set_user("Administrator")


def today_range():
	today_date = today()
	return today_date, today_date


def expired_range():
	today_date = today()
	return add_days(today_date, -30), add_days(today_date, -1)


def future_range():
	today_date = today()
	return add_days(today_date, 1), add_days(today_date, 30)
