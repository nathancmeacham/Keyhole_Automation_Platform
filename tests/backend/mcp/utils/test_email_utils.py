# Keyhole_Automation_Platform\tests\backend\mcp\utils\test_email_utils.py

from unittest.mock import patch
from backend.mcp.utils.email_utils import send_email

def test_send_email_success():
    with patch("backend.mcp.utils.email_utils.smtplib.SMTP_SSL") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        instance.send_message.return_value = True

        result = send_email("nathan@keyholesolution.com", "Mock Success", "✅ This is a mock test.")
        assert result is True

def test_send_email_failure():
    with patch("backend.mcp.utils.email_utils.smtplib.SMTP_SSL") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        instance.send_message.side_effect = Exception("Simulated error")

        result = send_email("nobody@example.com", "Mock Failure", "❌ This should fail.")
        assert result is False
