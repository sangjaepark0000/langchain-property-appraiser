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
      ? '질문을 처리하는 중입니다'
      : statusKind === 'insufficient_evidence'
        ? '근거가 충분하지 않습니다'
        : statusKind === 'error'
          ? '채팅 오류'
          : '준비됨'
  );
</script>

<aside class="status {statusKind}" data-testid="status-panel" aria-label="상태 패널" aria-live="polite">
  <strong>{headline}</strong>
  <p>{statusMessage}</p>
  {#if statusKind === 'error'}
    <small>백엔드에 연결된 뒤 다시 시도하세요.</small>
  {:else}
    <small>대화 ID: {conversationId ?? '새 대화'}</small>
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
