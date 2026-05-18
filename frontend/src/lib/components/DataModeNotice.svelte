<script lang="ts">
  type Props = {
    dataMode?: string | null;
    insufficientEvidenceReason?: string | null;
  };

  let { dataMode = 'unknown', insufficientEvidenceReason = null }: Props = $props();

  function modeLabel(mode: string | null | undefined): string {
    return mode && mode.trim() ? mode : 'unknown';
  }

  let currentMode = $derived(modeLabel(dataMode));
  let isOfficial = $derived(currentMode === 'official');
</script>

<section class:official={isOfficial} class="notice" data-testid="data-mode-notice" aria-label="데이터 출처와 안전 안내">
  <strong>데이터 모드: {currentMode}</strong>
  {#if !isOfficial}
    <p>샘플, 사용자 제공, 또는 출처 불명 데이터는 공식 판단이 아닙니다. 법률 판단이나 감정평가 적정성 판단이 아니라 참고용으로만 보세요.</p>
  {:else}
    <p>공식 출처로 표시된 데이터를 사용했지만, 이 답변은 참고용이며 최종 법률 판단이 아닙니다.</p>
  {/if}
  {#if insufficientEvidenceReason}
    <p class="reason">{insufficientEvidenceReason}</p>
  {/if}
</section>

<style>
  .notice {
    margin-top: 0.75rem;
    border: 1px solid #f0c36a;
    border-radius: 0.75rem;
    background: #fff8e6;
    color: #4a3411;
    padding: 0.75rem;
  }

  .notice.official {
    border-color: #91c79c;
    background: #edf8ef;
    color: #173d20;
  }

  p {
    margin: 0.35rem 0 0;
  }

  .reason {
    font-weight: 700;
  }
</style>
