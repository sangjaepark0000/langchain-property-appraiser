<script lang="ts">
  export type ChatMessage = {
    role: 'assistant' | 'user';
    content: string;
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
      <p>{message.content}</p>
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
</style>
