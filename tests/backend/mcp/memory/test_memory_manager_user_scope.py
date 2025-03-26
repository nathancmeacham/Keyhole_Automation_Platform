# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_memory_manager_user_scope.py

import pytest
from backend.mcp.memory.memory_singleton import memory_manager

TEST_USER_ID = "test_user_123"

def test_user_specific_fact_storage():
    memory_manager.store_fact("city", "Tbilisi", user_id=TEST_USER_ID)
    result = memory_manager.retrieve_fact("city", user_id=TEST_USER_ID)
    assert result == "Tbilisi"

def test_user_fact_overwrite():
    memory_manager.store_fact("language", "Georgian", user_id=TEST_USER_ID)
    result1 = memory_manager.retrieve_fact("language", user_id=TEST_USER_ID)
    assert result1 == "Georgian"

    memory_manager.store_fact("language", "English", user_id=TEST_USER_ID)
    result2 = memory_manager.retrieve_fact("language", user_id=TEST_USER_ID)
    assert result2 == "English"
    assert result2 != result1

def test_user_missing_fact_returns_none():
    result = memory_manager.retrieve_fact("unknown_key_abc", user_id=TEST_USER_ID)
    assert result is None

def test_user_specific_memory_storage_and_retrieval():
    query = "Tell me about the banana stand."
    context_text = "There is always money in the banana stand."
    metadata = {"type": "quote", "source": "Arrested Development"}

    memory_manager.store_memory(context_text, metadata, user_id=TEST_USER_ID)
    results = memory_manager.retrieve_memory(query, memory_type="quote", user_id=TEST_USER_ID)

    assert isinstance(results, list)
    assert any("banana" in r.page_content.lower() for r in results)

def test_user_list_all_facts():
    facts = memory_manager.list_all_facts(user_id=TEST_USER_ID)
    assert isinstance(facts, dict)
    assert "city" in facts or "language" in facts
