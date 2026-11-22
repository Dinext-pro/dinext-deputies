"""The first authenticated user survives successive deputy account switches."""

from unittest.mock import Mock, patch

import frappe

from dinext_deputies.overrides.user import impersonate_with_delegate
from dinext_deputies.tests.test_utils import DeputiesTestCase


class TestDelegatedSessionAudit(DeputiesTestCase):
	def test_following_switch_retains_the_initial_user(self):
		frappe.set_user("Administrator")
		frappe.session.data = frappe._dict(impersonated_by="original@example.com")
		manager = Mock()
		session = Mock()
		with (
			patch.object(frappe.local, "login_manager", manager, create=True),
			patch.object(frappe.local, "session_obj", session, create=True),
			patch("dinext_deputies.overrides.user.can_impersonate_as", return_value=True),
			patch.object(frappe, "get_doc"),
			patch.object(frappe, "new_doc"),
		):
			impersonate_with_delegate("next@example.com", "Temporary replacement")
		manager.impersonate.assert_called_once_with("next@example.com")
		session.set_impersonated.assert_called_once_with("original@example.com")
