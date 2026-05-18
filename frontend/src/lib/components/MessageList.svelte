<script lang="ts">
  import CitationPanel, { type Citation } from './CitationPanel.svelte';
  import DataModeNotice from './DataModeNotice.svelte';

  export type ChatMessage = {
    role: 'assistant' | 'user';
    content: string;
    citations?: Citation[];
    dataMode?: string;
    insufficientEvidenceReason?: string | null;
  };

  type Props = {
    messages: ChatMessage[];
  };

  let { messages }: Props = $props();
</script>

<div class="messages" data-testid="message-list" aria-live="polite">
  {#each messages as message}
    <article class:assistant={message.role === 'assistant'} class:user={message.role === 'user'}>
      <span>{message.role}</span>
      <p class="answer-body">{message.content}</p>
      {#if message.role === 'assistant' && ((message.dataMode && message.dataMode !== 'none') || message.insufficientEvidenceReason)}
        <DataModeNotice dataMode={message.dataMode} insufficientEvidenceReason={message.insufficientEvidenceReason} />
        <p class="safety-copy">참고용 답변입니다. 법률 위반 여부나 감정평가 적정성에 대한 최종 판단으로 사용하지 마세요.</p>
      {/if}
      {#if message.role === 'assistant' && message.citations}
        <CitationPanel citations={message.citations} />
      {/if}
    </article>
  {/each}
</div>

<style>
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

  .answer-body {
    margin: 0;
  }

  .safety-copy {
    margin: 0.65rem 0 0;
    color: #53617a;
    font-size: 0.9rem;
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
</style>
