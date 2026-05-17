<script lang="ts">
  export type Citation = {
    source_name?: string | null;
    source_path?: string | null;
    chunk_index?: number | string | null;
    data_mode?: string | null;
    [key: string]: unknown;
  };

  type Props = {
    citations?: Citation[];
  };

  let { citations = [] }: Props = $props();

  function field(value: unknown): string {
    if (value === null || value === undefined || value === '') return 'unknown';
    return String(value);
  }
</script>

{#if citations.length > 0}
  <section class="citations" data-testid="citation-panel" aria-label="Citations and source evidence">
    <h2>Sources</h2>
    <ol>
      {#each citations as citation}
        <li>
          <dl>
            <div>
              <dt>Source name</dt>
              <dd>{field(citation.source_name)}</dd>
            </div>
            <div>
              <dt>Source path</dt>
              <dd>{field(citation.source_path)}</dd>
            </div>
            <div>
              <dt>Chunk index</dt>
              <dd>{field(citation.chunk_index)}</dd>
            </div>
            <div>
              <dt>Data mode</dt>
              <dd>{field(citation.data_mode)}</dd>
            </div>
          </dl>
        </li>
      {/each}
    </ol>
  </section>
{/if}

<style>
  .citations {
    margin-top: 0.85rem;
    border-top: 1px solid rgb(73 104 216 / 20%);
    padding-top: 0.75rem;
  }

  h2 {
    margin: 0 0 0.5rem;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  ol {
    display: grid;
    gap: 0.6rem;
    margin: 0;
    padding-left: 1.2rem;
  }

  dl {
    display: grid;
    gap: 0.25rem;
    margin: 0;
  }

  div {
    display: grid;
    grid-template-columns: 7rem minmax(0, 1fr);
    gap: 0.5rem;
  }

  dt {
    color: #53617a;
    font-weight: 700;
  }

  dd {
    margin: 0;
    overflow-wrap: anywhere;
  }
</style>
