from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_chat_input_component_supports_submit_guard_and_reset():
    component = (FRONTEND / "src" / "lib" / "components" / "ChatInput.svelte").read_text()

    assert 'data-testid="chat-input"' in component
    assert "trim()" in component
    assert "if (!trimmed)" in component
    assert "question = ''" in component
    assert "on:submit|preventDefault" in component
    assert "type=\"submit\"" in component


def test_message_list_component_renders_ordered_role_distinguished_messages():
    component = (FRONTEND / "src" / "lib" / "components" / "MessageList.svelte").read_text()

    assert 'data-testid="message-list"' in component
    assert "{#each messages as message" in component
    assert "message.role === 'assistant'" in component
    assert "message.role === 'user'" in component
    assert "aria-live=\"polite\"" in component


def test_page_composes_chat_input_and_message_list():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "import ChatInput" in page
    assert "import MessageList" in page
    assert "<MessageList {messages}" in page
    assert "<ChatInput onSubmit={submitQuestion}" in page
    assert "messages = [...messages, { role: 'user'" in page
    assert "messages = [...messages, { role: 'assistant'" in page
