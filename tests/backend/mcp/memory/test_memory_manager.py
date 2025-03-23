# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_memory_manager.py
# ✅ Unit tests for memory_manager.py

import unittest
from backend.mcp.memory.memory_manager import (
    init_memory_collection,
    init_fact_collection,
    store_memory,
    retrieve_memory,
    store_fact,
    retrieve_fact,
    recreate_collection,
    EMBEDDING_DIMENSIONS,
    COLLECTION_MEMORY,
    COLLECTION_FACTS
)

class TestMemoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure clean test environment
        recreate_collection(COLLECTION_MEMORY, EMBEDDING_DIMENSIONS)
        recreate_collection(COLLECTION_FACTS, EMBEDDING_DIMENSIONS)
        init_memory_collection()
        init_fact_collection()

    def test_store_and_retrieve_memory(self):
        """Store and retrieve a memory item with metadata filtering."""
        text = "There is always money in the banana stand."
        metadata = {"type": "quote", "origin": "Arrested Development"}
        store_memory(text, metadata)

        results = retrieve_memory("banana", memory_type="quote", top_k=5)
        self.assertIsInstance(results, list)
        self.assertTrue(any("banana" in r.page_content.lower() for r in results))

    def test_store_and_retrieve_fact(self):
        """Store a fact and retrieve it accurately."""
        store_fact("CEO", "Michael Bluth")
        result = retrieve_fact("CEO")
        self.assertEqual(result, "Michael Bluth")

    def test_overwrite_fact(self):
        """Ensure that updating a fact removes the old one."""
        store_fact("budget", "$500")
        first_result = retrieve_fact("budget")
        self.assertEqual(first_result, "$500")

        store_fact("budget", "$750")
        second_result = retrieve_fact("budget")
        self.assertEqual(second_result, "$750")
        self.assertNotEqual(second_result, first_result)

    def test_retrieve_missing_fact(self):
        """Returns None when fact key does not exist."""
        result = retrieve_fact("nonexistent_key_xyz")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
