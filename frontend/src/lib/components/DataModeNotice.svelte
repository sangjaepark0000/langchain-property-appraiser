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

<section class:official={isOfficial} class="notice" data-testid="data-mode-notice" aria-label="Data mode and safety notice">
  <strong>Data mode: {currentMode}</strong>
  {#if !isOfficial}
    <p>sample, user_provided, or unknown data means this response is not an official determination. Treat it as a reference aid, not a legal or appraisal suitability decision.</p>
  {:else}
    <p>This response uses official-labeled data, but remains a reference aid and not a final legal determination.</p>
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
