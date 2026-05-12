from pathlib import Path


def test_required_project_files_exist():
    required_paths = [
        "api/main.py",
        "crew_ai/crew_runner.py",
        "crew_ai/agents.py",
        "crew_ai/tasks.py",
        "crew_ai/tools.py",
        "rag/retriever.py",
        "rag/ingest.py",
        "data/faiss_index",
        "Dockerfile",
        "requirements-docker.txt",
    ]

    for path in required_paths:
        assert Path(path).exists(), f"Missing required path: {path}"
