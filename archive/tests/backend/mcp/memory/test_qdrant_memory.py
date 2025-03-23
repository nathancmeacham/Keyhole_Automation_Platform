# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_qdrant_memory.py
# ✅ Unit tests for backend.mcp.memory.qdrant_memory
# Archived test file for the Qdrant memory module. This module is no longer used in the project.
# The Qdrant memory module was replaced by Keyhole_Automation_Platform\mcp\memory\memory_manager.py

import unittest
from backend.mcp.memory.qdrant_memory import init_memory, store_memory, retrieve_memory

class TestQdrantMemory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the memory collection before running tests."""
        init_memory()

    def test_store_and_retrieve_memory(self):
        """Test storing and retrieving a memory item."""
        test_input = "There’s always money in the banana stand."
        store_memory(test_input)
        results = retrieve_memory("banana")
        self.assertTrue(any("banana" in r.lower() for r in results))

    def test_empty_result(self):
        """Test querying something not in memory."""
        results = retrieve_memory("completely unrelated query string")
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()
