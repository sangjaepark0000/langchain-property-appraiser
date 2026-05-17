# Review Prompt: Pi Web Search Extension

Please run an adversarial code review of the changed file with no additional conversation context.

## Changed file

- `/home/psj/.pi/agent/extensions/web-search.ts`

## Review focus

- Runtime compatibility with Pi extension API
- TypeScript/typebox schema correctness
- Brave Search API request correctness
- Error handling and missing API key behavior
- Security/privacy concerns around search queries and API keys
- Whether the model prompt guidance is clear enough

## Code

```ts
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

type BraveSearchResult = {
	title?: string;
	url?: string;
	description?: string;
	age?: string;
};

function formatResults(results: BraveSearchResult[]): string {
	if (results.length === 0) {
		return "No web search results found.";
	}

	return results
		.map((result, index) => {
			const title = result.title ?? "Untitled";
			const url = result.url ?? "No URL";
			const description = result.description ?? "";
			const age = result.age ? `\nPublished/age: ${result.age}` : "";
			return `${index + 1}. ${title}\n${url}${age}\n${description}`.trim();
		})
		.join("\n\n");
}

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "web_search",
		label: "Web Search",
		description: "Search the web for current information using Brave Search API.",
		promptSnippet: "Search the web for current information.",
		promptGuidelines: [
			"Use web_search when the user asks for current information, latest versions, current documentation, or recent facts.",
			"When using web_search, cite result URLs in the response and distinguish searched facts from local project facts.",
		],
		parameters: Type.Object({
			query: Type.String({ description: "Search query" }),
			count: Type.Optional(
				Type.Number({
					description: "Number of results to return, from 1 to 10. Defaults to 5.",
					minimum: 1,
					maximum: 10,
				}),
			),
		}),
		async execute(_toolCallId, params, signal) {
			const apiKey = process.env.BRAVE_SEARCH_API_KEY;
			if (!apiKey) {
				return {
					content: [
						{
							type: "text" as const,
							text:
								"BRAVE_SEARCH_API_KEY is not set. Create a Brave Search API key, export it, then run /reload in pi.",
						},
					],
					details: { missingEnv: "BRAVE_SEARCH_API_KEY" },
					isError: true,
				};
			}

			const count = Math.max(1, Math.min(10, Math.floor(params.count ?? 5)));
			const url = new URL("https://api.search.brave.com/res/v1/web/search");
			url.searchParams.set("q", params.query);
			url.searchParams.set("count", String(count));

			const response = await fetch(url, {
				signal,
				headers: {
					Accept: "application/json",
					"Accept-Encoding": "gzip",
					"X-Subscription-Token": apiKey,
				},
			});

			if (!response.ok) {
				const body = await response.text().catch(() => "");
				return {
					content: [
						{
							type: "text" as const,
							text: `Web search failed: ${response.status} ${response.statusText}${body ? `\n${body}` : ""}`,
						},
					],
					details: { status: response.status, statusText: response.statusText, body },
					isError: true,
				};
			}

			const data = await response.json();
			const results: BraveSearchResult[] = data.web?.results ?? [];

			return {
				content: [{ type: "text" as const, text: formatResults(results) }],
				details: { query: params.query, count, results },
			};
		},
	});
}
```
