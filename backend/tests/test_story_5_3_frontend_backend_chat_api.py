from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_chat_api_client_posts_question_and_optional_conversation_id():
    client = (FRONTEND / "src" / "lib" / "api" / "chat.ts").read_text()

    assert "export async function sendChatMessage" in client
    assert "question: string" in client
    assert "conversation_id?: number" in client
    assert "fetch(`${API_BASE_URL}/chat`" in client
    assert "method: 'POST'" in client
    assert "JSON.stringify(request)" in client
    assert "response.ok" in client


def test_page_sends_first_and_followup_questions_with_conversation_id():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "let conversationId: number | undefined" in page
    assert "sendChatMessage({ question, conversation_id: conversationId })" in page
    assert "conversationId = response.conversation_id" in page
    assert "messages = [...messages, { role: 'assistant', content: response.answer }]" in page


def test_page_shows_explicit_error_without_breaking_message_list():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "catch (error)" in page
    assert "Chat error:" in page
    assert "messages = [...messages, { role: 'assistant', content: errorMessage }]" in page
    assert "isSubmitting = false" in page
