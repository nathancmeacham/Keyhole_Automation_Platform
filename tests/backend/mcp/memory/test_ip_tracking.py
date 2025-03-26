# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_ip_tracking.py

import unittest
from backend.mcp.memory.memory_singleton import memory_manager

class TestIPTracking(unittest.TestCase):
    def setUp(self):
        self.guest_user_id = "guest"
        self.ip_test_1 = "192.168.1.101"
        self.ip_test_2 = "192.168.1.102"
        self.logged_in_user = "user_5678"

    def test_store_unique_guest_ips(self):
        """✅ Guest IPs should be stored only once per unique IP."""
        memory_manager.track_guest_ip(self.ip_test_1)
        memory_manager.track_guest_ip(self.ip_test_1)  # duplicate
        memory_manager.track_guest_ip(self.ip_test_2)

        ip_set = memory_manager.list_guest_ips()
        self.assertIn(self.ip_test_1, ip_set)
        self.assertIn(self.ip_test_2, ip_set)
        self.assertEqual(len(ip_set), 2)

    def test_store_logged_in_user_ips(self):
        """✅ Logged-in user IPs should accumulate per user ID."""
        memory_manager.track_user_ip(self.logged_in_user, self.ip_test_1)
        memory_manager.track_user_ip(self.logged_in_user, self.ip_test_2)

        ips = memory_manager.get_user_ips(self.logged_in_user)
        self.assertIn(self.ip_test_1, ips)
        self.assertIn(self.ip_test_2, ips)
        self.assertEqual(len(ips), 2)

    def test_logged_in_user_duplicate_ip(self):
        """✅ Duplicate IPs should not appear twice for the same user."""
        memory_manager.track_user_ip(self.logged_in_user, self.ip_test_1)
        memory_manager.track_user_ip(self.logged_in_user, self.ip_test_1)

        ips = memory_manager.get_user_ips(self.logged_in_user)
        self.assertEqual(len(ips), 2)  # test_1 and test_2 already exist, should not duplicate

if __name__ == "__main__":
    unittest.main()
