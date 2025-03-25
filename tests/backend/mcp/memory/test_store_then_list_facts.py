# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_store_then_list_facts.py

from backend.mcp.memory.memory_manager import MemoryManager
import pytest

def test_store_then_list_fact():
    mm = MemoryManager()
    test_key = "test_user"
    test_value = "Nathan"

    # Store fact
    mm.store_fact(test_key, test_value)

    # List all facts
    facts = mm.list_all_facts()

    assert test_key in facts, f"Expected fact '{test_key}' not found."
    assert facts[test_key] == test_value, f"Value mismatch: expected '{test_value}', got '{facts[test_key]}'"

    print(f"\n✅ {test_key} = {facts[test_key]} found in fact list.")
