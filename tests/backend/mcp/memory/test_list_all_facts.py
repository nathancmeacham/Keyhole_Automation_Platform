# Keyhole_Automation_Platform\tests\backend\mcp\memory\test_list_all_facts.py

from backend.mcp.memory.memory_manager import MemoryManager

def test_list_all_facts():
    mm = MemoryManager()
    print("\n🧪 Retrieving all facts from Qdrant...\n")

    facts = mm.list_all_facts()

    if not facts:
        print("⚠️ No facts found.")
    else:
        print(f"✅ Found {len(facts)} facts:")
        for key, value in facts.items():
            print(f"🔑 {key} = {value}")

    # Basic assertion to pass the test
    assert isinstance(facts, dict)
