<script lang="ts">
  import { sendChatMessage } from '$lib/api/chat';
  import ChatInput from '$lib/components/ChatInput.svelte';
  import type { Citation } from '$lib/components/CitationPanel.svelte';
  import MessageList, { type ChatMessage } from '$lib/components/MessageList.svelte';
  import StatusPanel, { type ChatStatus } from '$lib/components/StatusPanel.svelte';

  type CitationForMessage = Citation;

  let statusKind: ChatStatus = 'ready';
  let status = 'Ready';
  let isSubmitting = false;
  let conversationId: number | undefined;
  let messages: ChatMessage[] = [
    {
      role: 'assistant',
      content: 'Ask a property appraisal question to start a grounded conversation.'
    }
  ];

  async function submitQuestion(question: string) {
    messages = [...messages, { role: 'user', content: question }];
    statusKind = 'loading';
    status = 'Waiting for backend /chat response...';
    isSubmitting = true;

    try {
      const response = await sendChatMessage({ question, conversation_id: conversationId });
      conversationId = response.conversation_id;
      // Base assistant append shape: messages = [...messages, { role: 'assistant', content: response.answer }]
      messages = [
        ...messages,
        {
          role: 'assistant',
          content: response.answer,
          citations: response.citations as CitationForMessage[],
          dataMode: response.data_mode,
          insufficientEvidenceReason: response.insufficient_evidence_reason
        }
      ];
      statusKind = response.insufficient_evidence ? 'insufficient_evidence' : 'ready';
      status = response.insufficient_evidence
        ? `Insufficient evidence: ${response.insufficient_evidence_reason ?? 'reason unavailable'}`
        : `Answered from ${response.data_mode} data`;
    } catch (error) {
      const errorMessage = error instanceof Error ? `Chat error: ${error.message}` : 'Chat error: unexpected failure';
      statusKind = 'error';
      status = errorMessage;
      messages = [...messages, { role: 'assistant', content: errorMessage }];
    } finally {
      isSubmitting = false;
    }
  }
</script>

<svelte:head>
  <title>Property Appraiser Chat</title>
</svelte:head>

<main class="shell">
  <section class="hero">
    <p class="eyebrow">LangChain Property Appraiser</p>
    <h1>Property Appraiser Chat</h1>
    <p>Multi-turn RAG workspace for appraisal questions, citations, and evidence status.</p>
  </section>

  <section class="chat-panel" aria-label="Chat workspace">
    <div data-testid="message-list">
      <MessageList {messages} />
    </div>
    <div data-testid="chat-input">
      <ChatInput onSubmit={submitQuestion} disabled={isSubmitting} />
    </div>

    <div data-testid="status-panel">
      <StatusPanel {statusKind} statusMessage={status} {conversationId} />
    </div>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, sans-serif;
    background: #f5f7fb;
    color: #172033;
  }

  .shell {
    min-height: 100vh;
    display: grid;
    grid-template-columns: minmax(16rem, 24rem) minmax(0, 1fr);
    gap: 2rem;
    padding: 2rem;
  }

  .hero,
  .chat-panel {
    background: white;
    border: 1px solid #dfe5ef;
    border-radius: 1.25rem;
    box-shadow: 0 18px 50px rgb(23 32 51 / 8%);
  }

  .hero {
    padding: 2rem;
  }

  .eyebrow {
    color: #4968d8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .chat-panel {
    display: grid;
    grid-template-rows: minmax(20rem, 1fr) auto auto;
    overflow: hidden;
  }

  @media (max-width: 820px) {
    .shell {
      grid-template-columns: 1fr;
    }
  }
</style>
