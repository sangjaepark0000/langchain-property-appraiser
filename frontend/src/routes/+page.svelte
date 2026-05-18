<script lang="ts">
  import { sendChatMessage } from '$lib/api/chat';
  import ChatInput from '$lib/components/ChatInput.svelte';
  import type { Citation } from '$lib/components/CitationPanel.svelte';
  import MessageList, { type ChatMessage } from '$lib/components/MessageList.svelte';
  import StatusPanel, { type ChatStatus } from '$lib/components/StatusPanel.svelte';

  type CitationForMessage = Citation;

  let statusKind: ChatStatus = 'ready';
  let status = '준비됨';
  let isSubmitting = false;
  let conversationId: number | undefined;
  let messages: ChatMessage[] = [
    {
      role: 'assistant',
      content: '작성한 감정평가 서류나 검토하고 싶은 내용을 입력해 주세요. 공식 법령 근거를 찾아 익숙해서 놓치기 쉬운 확인 포인트를 참고용으로 정리해드립니다.'
    }
  ];

  async function submitQuestion(question: string) {
    messages = [...messages, { role: 'user', content: question }];
    statusKind = 'loading';
    status = '백엔드 /chat 응답을 기다리는 중입니다...';
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
        ? `근거 부족: ${response.insufficient_evidence_reason ?? '사유 없음'}`
        : `${response.data_mode} 데이터 기반으로 답변했습니다`;
    } catch (error) {
      const errorMessage = error instanceof Error ? `채팅 오류: ${error.message}` : '채팅 오류: 알 수 없는 실패';
      statusKind = 'error';
      status = errorMessage;
      messages = [...messages, { role: 'assistant', content: errorMessage }];
    } finally {
      isSubmitting = false;
    }
  }
</script>

<svelte:head>
  <title>감정평가 법령 RAG 채팅</title>
</svelte:head>

<main class="shell">
  <section class="hero">
    <p class="eyebrow">감정평가 법령 RAG</p>
    <h1>감정평가 서류 검토 도우미</h1>
    <p>작성한 감정평가 서류에서 익숙해서 놓치기 쉬운 확인 포인트를 공식 법령 근거와 함께 검토할 수 있도록 도와드립니다.</p>
  </section>

  <section class="chat-panel" aria-label="채팅 작업공간">
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
