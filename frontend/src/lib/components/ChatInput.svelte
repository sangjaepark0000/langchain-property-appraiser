<script lang="ts">
  type Props = {
    onSubmit: (question: string) => void | Promise<void>;
    disabled?: boolean;
  };

  let { onSubmit, disabled = false }: Props = $props();
  let question = $state('');

  async function submit() {
    const trimmed = question.trim();
    if (!trimmed) return;

    question = '';
    await onSubmit(trimmed);
  }
</script>

<form
  class="composer"
  data-testid="chat-input"
  onsubmit={(event) => {
    event.preventDefault();
    void submit();
  }}
>
  <label for="question">질문</label>
  <div>
    <input
      id="question"
      bind:value={question}
      disabled={disabled}
      placeholder="감정평가 법령이나 근거에 대해 질문하세요"
      autocomplete="off"
    />
    <button type="submit" disabled={disabled || !question.trim()}>보내기</button>
  </div>
</form>

<style>
  .composer {
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

  button:disabled,
  input:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
</style>
