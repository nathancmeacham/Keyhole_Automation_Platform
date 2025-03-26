# Keyhole_Automation_Platform\tests\backend\mcp\utils\test_auth_utils.py

import unittest
from backend.mcp.utils import auth_utils

class TestAuthUtils(unittest.TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "SuperSecure123!"

    def test_password_hashing_and_verification(self):
        hashed = auth_utils.hash_password(self.password)
        self.assertTrue(auth_utils.verify_password(self.password, hashed))
        self.assertFalse(auth_utils.verify_password("wrongpassword", hashed))

    def test_jwt_token_creation_and_decoding(self):
        data = {"sub": self.email, "role": "user"}
        token = auth_utils.create_jwt_token(data)
        decoded = auth_utils.decode_jwt_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded.get("sub"), self.email)

    def test_email_token_creation_and_confirmation(self):
        token = auth_utils.create_email_token(self.email)
        confirmed_email = auth_utils.confirm_email_token(token)
        self.assertEqual(confirmed_email, self.email)

if __name__ == "__main__":
    unittest.main()
