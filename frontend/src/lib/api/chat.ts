export type ChatRequest = {
  question: string;
  conversation_id?: number;
};

export type ChatResponse = {
  conversation_id: number;
  message_id: number;
  answer: string;
  citations: Record<string, unknown>[];
  data_mode: string;
  insufficient_evidence: boolean;
  insufficient_evidence_reason?: string | null;
  retrieval_trace: Record<string, unknown>;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status}`);
  }

  return response.json();
}
