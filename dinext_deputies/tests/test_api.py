import frappe

from dinext_deputies.api import get_delegatable_users
from dinext_deputies.dinext_deputies.doctype.user_delegate.user_delegate import can_impersonate_as
from dinext_deputies.tests.test_utils import (
	DeputiesTestCase,
	assert_sorted_by_full_name,
	assert_user_fields,
	create_test_user,
	create_user_delegate,
	expired_range,
	future_range,
	test_email,
	today_range,
)


class TestGetDelegatableUsers(DeputiesTestCase):
	def test_system_manager_returns_enabled_users_sorted_by_full_name(self):
		sysmgr = test_email("sysmgr")
		create_test_user(sysmgr, roles=("System Manager",))

		frappe.set_user(sysmgr)
		result = get_delegatable_users()

		self.assertTrue(result)
		for row in result:
			assert_user_fields(self, row)
			self.assertTrue(frappe.db.get_value("User", row["name"], "enabled"))
		assert_sorted_by_full_name(self, result)

	def test_administrator_returns_enabled_users_sorted_by_full_name(self):
		frappe.set_user("Administrator")
		result = get_delegatable_users()

		self.assertTrue(result)
		for row in result:
			assert_user_fields(self, row)
			self.assertTrue(frappe.db.get_value("User", row["name"], "enabled"))
		assert_sorted_by_full_name(self, result)

	def test_delegate_returns_active_delegator(self):
		delegate = test_email("delegate_active")
		delegator = test_email("delegator_active")
		create_test_user(delegate)
		create_test_user(delegator, enabled=1)
		from_date, to_date = today_range()
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		result = get_delegatable_users()

		self.assertEqual(len(result), 1)
		assert_user_fields(self, result[0])
		self.assertEqual(result[0]["name"], delegator)
		self.assertEqual(result[0]["full_name"], frappe.db.get_value("User", delegator, "full_name"))

	def test_delegate_excludes_delegator_outside_date_range(self):
		delegate = test_email("delegate_dates")
		delegator = test_email("delegator_dates")
		create_test_user(delegate)
		create_test_user(delegator)
		from_date, to_date = expired_range()
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		result = get_delegatable_users()

		names = {row["name"] for row in result}
		self.assertNotIn(delegator, names)

	def test_delegate_excludes_disabled_delegator(self):
		delegate = test_email("delegate_disabled")
		delegator = test_email("delegator_disabled")
		create_test_user(delegate)
		create_test_user(delegator, enabled=0)
		from_date, to_date = today_range()
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		result = get_delegatable_users()

		names = {row["name"] for row in result}
		self.assertNotIn(delegator, names)

	def test_delegate_without_delegations_returns_empty_list(self):
		delegate = test_email("delegate_empty")
		create_test_user(delegate)

		frappe.set_user(delegate)
		result = get_delegatable_users()

		self.assertEqual(result, [])

	def test_delegate_may_return_duplicate_delegator_rows(self):
		delegate = test_email("delegate_dup")
		delegator = test_email("delegator_dup")
		create_test_user(delegate)
		create_test_user(delegator)
		from_date, to_date = today_range()
		create_user_delegate(delegate, delegator, from_date, to_date)
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		result = get_delegatable_users()

		delegator_rows = [row for row in result if row["name"] == delegator]
		self.assertGreaterEqual(len(delegator_rows), 2)


class TestCanImpersonateAs(DeputiesTestCase):
	def test_administrator_can_impersonate_any_user(self):
		target = test_email("target_admin")
		create_test_user(target)

		frappe.set_user("Administrator")
		self.assertTrue(can_impersonate_as(target))

	def test_delegate_can_impersonate_active_delegator(self):
		delegate = test_email("delegate_can")
		delegator = test_email("delegator_can")
		create_test_user(delegate)
		create_test_user(delegator)
		from_date, to_date = today_range()
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		self.assertTrue(can_impersonate_as(delegator))

	def test_delegate_cannot_impersonate_without_delegation(self):
		delegate = test_email("delegate_no_perm")
		delegator = test_email("delegator_no_perm")
		create_test_user(delegate)
		create_test_user(delegator)

		frappe.set_user(delegate)
		self.assertFalse(can_impersonate_as(delegator))

	def test_delegate_cannot_impersonate_when_dates_outside_today(self):
		delegate = test_email("delegate_future")
		delegator = test_email("delegator_future")
		create_test_user(delegate)
		create_test_user(delegator)
		from_date, to_date = future_range()
		create_user_delegate(delegate, delegator, from_date, to_date)

		frappe.set_user(delegate)
		self.assertFalse(can_impersonate_as(delegator))
