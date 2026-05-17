from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_sveltekit_frontend_project_files_exist():
    assert (FRONTEND / "package.json").exists()
    assert (FRONTEND / "svelte.config.js").exists()
    assert (FRONTEND / "vite.config.ts").exists()
    assert (FRONTEND / "src" / "routes" / "+page.svelte").exists()
    assert (FRONTEND / "src" / "lib" / "api" / "chat.ts").exists()


def test_default_page_has_chat_layout_regions():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert 'data-testid="message-list"' in page
    assert 'data-testid="chat-input"' in page
    assert 'data-testid="status-panel"' in page
    assert "Property Appraiser Chat" in page


def test_frontend_keeps_simple_api_structure_without_global_state_manager():
    package_json = (FRONTEND / "package.json").read_text()
    api_client = (FRONTEND / "src" / "lib" / "api" / "chat.ts").read_text()

    forbidden = ["redux", "zustand", "mobx", "xstate", "@ngrx"]
    assert all(dep not in package_json.lower() for dep in forbidden)
    assert "fetch(" in api_client
    assert "/chat" in api_client


def test_frontend_readme_documents_local_development():
    readme = (FRONTEND / "README.md").read_text().lower()

    assert "npm install" in readme
    assert "npm run dev" in readme
    assert "backend" in readme
