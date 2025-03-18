# codebase_snapshot.py
import os
from git import Repo, InvalidGitRepositoryError
from memory_manager import store_memory

def snapshot_and_commit(repo_path='.', commit_message='Snapshot commit'):
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print("❌ Not a git repository. Please initialize with 'git init'.")
        return

    repo.git.add(all=True)
    repo.index.commit(commit_message)
    commit_hash = repo.head.commit.hexsha
    print(f"✅ Committed codebase snapshot: {commit_hash}")

    store_memory(
        text=f"Codebase snapshot committed: {commit_hash}",
        metadata={"type": "codebase_snapshot", "commit_hash": commit_hash}
    )