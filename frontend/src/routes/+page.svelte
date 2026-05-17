<script lang="ts">
  import { sendChatMessage } from '$lib/api/chat';

  type Message = {
    role: 'assistant' | 'user';
    content: string;
  };

  let question = '';
  let status = 'Ready';
  let conversationId: number | undefined;
  let messages: Message[] = [
    {
      role: 'assistant',
      content: 'Ask a property appraisal question to start a grounded conversation.'
    }
  ];

  async function submitQuestion() {
    const trimmed = question.trim();
    if (!trimmed) return;

    messages = [...messages, { role: 'user', content: trimmed }];
    question = '';
    status = 'Waiting for backend /chat response...';

    try {
      const response = await sendChatMessage({ question: trimmed, conversation_id: conversationId });
      conversationId = response.conversation_id;
      messages = [...messages, { role: 'assistant', content: response.answer }];
      status = response.insufficient_evidence
        ? `Insufficient evidence: ${response.insufficient_evidence_reason ?? 'reason unavailable'}`
        : `Answered from ${response.data_mode} data`;
    } catch (error) {
      status = error instanceof Error ? error.message : 'Unexpected chat error';
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
    <div class="messages" data-testid="message-list" aria-live="polite">
      {#each messages as message}
        <article class:assistant={message.role === 'assistant'} class:user={message.role === 'user'}>
          <span>{message.role}</span>
          <p>{message.content}</p>
        </article>
      {/each}
    </div>

    <form class="composer" data-testid="chat-input" on:submit|preventDefault={submitQuestion}>
      <label for="question">Question</label>
      <div>
        <input id="question" bind:value={question} placeholder="Ask about a property or appraisal basis" />
        <button type="submit">Send</button>
      </div>
    </form>

    <aside class="status" data-testid="status-panel" aria-label="Status panel">
      <strong>Status</strong>
      <p>{status}</p>
      <small>Conversation: {conversationId ?? 'new'}</small>
    </aside>
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

  .messages {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
    overflow: auto;
  }

  article {
    max-width: 70ch;
    border-radius: 1rem;
    padding: 1rem;
  }

  article span {
    display: block;
    margin-bottom: 0.35rem;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
  }

  article p {
    margin: 0;
  }

  .assistant {
    align-self: flex-start;
    background: #eef3ff;
  }

  .user {
    align-self: flex-end;
    background: #18223a;
    color: white;
  }

  .composer,
  .status {
    border-top: 1px solid #dfe5ef;
    padding: 1rem 1.5rem;
  }

  .composer label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }

  .composer div {
    display: flex;
    gap: 0.75rem;
  }

  input {
    flex: 1;
    border: 1px solid #c9d3e3;
    border-radius: 999px;
    padding: 0.8rem 1rem;
  }

  button {
    border: 0;
    border-radius: 999px;
    background: #4968d8;
    color: white;
    cursor: pointer;
    font-weight: 700;
    padding: 0.8rem 1.2rem;
  }

  .status p {
    margin: 0.35rem 0;
  }

  @media (max-width: 820px) {
    .shell {
      grid-template-columns: 1fr;
    }
  }
</style>
