# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_batch_memory.py

import time
import pytest
from backend.mcp.memory.memory_manager import MemoryManager

@pytest.fixture(scope="module")
def memory_manager():
    return MemoryManager()

def test_store_and_retrieve_fact(memory_manager):
    test_key = "name"
    test_value = "Nathan"

    memory_manager.store_fact(test_key, test_value)
    time.sleep(1)  # Small delay to ensure write is committed

    retrieved = memory_manager.retrieve_fact(test_key)
    assert retrieved == test_value, f"Expected '{test_value}', got '{retrieved}'"

def test_store_and_retrieve_memory(memory_manager):
    sample_text = "This is a test memory about MCP platform."
    memory_manager.store_memory(sample_text, metadata={"type": "test"})
    time.sleep(1)

    results = memory_manager.retrieve_memory("MCP", memory_type="test")
    assert results, "Expected at least one memory result"
    assert any("MCP" in mem.page_content for mem in results), "Memory content mismatch"
