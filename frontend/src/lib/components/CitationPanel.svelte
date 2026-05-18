<script lang="ts">
  export type Citation = {
    source_name?: string | null;
    source_path?: string | null;
    source_authority?: string | null;
    law_name?: string | null;
    article_number?: string | null;
    article_title?: string | null;
    effective_date?: string | null;
    revision_date?: string | null;
    law_level?: string | null;
    document_kind?: string | null;
    chunk_type?: string | null;
    change_type?: string | null;
    revision_marker?: string | null;
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

  function legalLabel(citation: Citation): string {
    const law = field(citation.law_name ?? citation.source_name);
    const article = field(citation.article_number);
    const title = field(citation.article_title);
    if (article === 'unknown') return law;
    if (title === 'unknown') return `${law} ${article}`;
    return `${law} ${article}(${title})`;
  }
</script>

{#if citations.length > 0}
  <section class="citations" data-testid="citation-panel" aria-label="Citations and source evidence">
    <h2>Sources</h2>
    <ol>
      {#each citations as citation}
        <li>
          <p class="legal-label">{legalLabel(citation)}</p>
          <dl>
            <div>
              <dt>Authority</dt>
              <dd>{field(citation.source_authority)}</dd>
            </div>
            <div>
              <dt>Effective</dt>
              <dd>{field(citation.effective_date)}</dd>
            </div>
            <div>
              <dt>Revision</dt>
              <dd>{field(citation.revision_date)}</dd>
            </div>
            <div>
              <dt>Source name</dt>
              <dd>{field(citation.source_name)}</dd>
            </div>
            <div>
              <dt>Article</dt>
              <dd>{field(citation.article_number)} {field(citation.article_title)}</dd>
            </div>
            <div>
              <dt>Document kind</dt>
              <dd>{field(citation.document_kind)}</dd>
            </div>
            <div>
              <dt>Chunk</dt>
              <dd>{field(citation.chunk_type)} #{field(citation.chunk_index)}</dd>
            </div>
            {#if citation.change_type && citation.change_type !== 'unknown'}
              <div>
                <dt>Change</dt>
                <dd>{field(citation.change_type)} {field(citation.revision_marker)}</dd>
              </div>
            {/if}
            <div>
              <dt>Source path</dt>
              <dd>{field(citation.source_path)}</dd>
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

  .legal-label {
    margin: 0 0 0.35rem;
    color: #24345f;
    font-weight: 800;
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
