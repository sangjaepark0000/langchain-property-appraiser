<script lang="ts">
  export type ChatStatus = 'ready' | 'loading' | 'insufficient_evidence' | 'error';

  type Props = {
    statusKind: ChatStatus;
    statusMessage: string;
    conversationId?: number;
  };

  let { statusKind, statusMessage, conversationId }: Props = $props();

  let headline = $derived(
    statusKind === 'loading'
      ? 'Processing your question'
      : statusKind === 'insufficient_evidence'
        ? 'Evidence is insufficient'
        : statusKind === 'error'
          ? 'Chat error'
          : 'Ready'
  );
</script>

<aside class="status {statusKind}" data-testid="status-panel" aria-label="Status panel" aria-live="polite">
  <strong>{headline}</strong>
  <p>{statusMessage}</p>
  {#if statusKind === 'error'}
    <small>Try again when the backend is reachable.</small>
  {:else}
    <small>Conversation: {conversationId ?? 'new'}</small>
  {/if}
</aside>

<style>
  .status {
    border-top: 1px solid #dfe5ef;
    padding: 1rem 1.5rem;
  }

  .status p {
    margin: 0.35rem 0;
  }

  .loading {
    background: #eef3ff;
  }

  .insufficient_evidence {
    background: #fff8e6;
  }

  .error {
    background: #fff1f0;
    color: #7d1b14;
  }
</style>
