# LinkedIn MCP server for Claude, ChatGPT and Codex — OutreachGenie

Connect Claude, ChatGPT, Claude Code, or Codex to your LinkedIn prospecting
workspace: look up and import prospects, organize lists, build outreach flows,
and prepare campaigns from chat. Hosted and OAuth-secured, with MCP access
included on the Free plan.

```
https://api.outreachgenie.ai/mcp
```

**[Add to Claude](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=OutreachGenie&connectorUrl=https%3A%2F%2Fapi.outreachgenie.ai%2Fmcp)** · [Website](https://www.outreachgenie.ai/linkedin-mcp) · [Developer docs](https://www.outreachgenie.ai/developers)

## Free saved-list audit skill

[OutreachGenie list audit](skills/outreachgenie-list-audit/SKILL.md) checks saved prospect lists against a saved outreach flow. It finds missing personalization values, list metadata gaps, overlong invitation notes/messages and incomplete membership captures. It reads existing data and produces local JSON/Markdown findings; it does not create or activate a campaign.

Install the skill for Codex in your project with the tested [Skills CLI](https://skills.sh/docs/cli) version:

```bash
DISABLE_TELEMETRY=1 npx skills@1.7.2 add Outreachgenie/outreachgenie-linkedin-mcp \
  --skill outreachgenie-list-audit --agent codex --copy
```

Or download the [v0.1.0 skill ZIP](https://github.com/Outreachgenie/outreachgenie-linkedin-mcp/releases/download/list-audit-v0.1.0/outreachgenie-list-audit-0.1.0.zip). Installing the skill files does not connect an OutreachGenie account or grant MCP permissions.

The included demonstration is fictional and needs no account or credentials. From a checkout of this repository, with Python 3.10 or newer:

```bash
cd skills/outreachgenie-list-audit
python3 scripts/audit.py --input fixtures/fictional-snapshot.json --output-dir ../outreachgenie-audit-demo
```

The output directory must not exist. Read the generated report before considering any follow-up work. Complete collection or zero findings does not certify readiness to send.

For a real audit, [open an OutreachGenie workspace](https://app.outreachgenie.ai/), select existing lists and a saved flow, and connect the hosted MCP server with `crm.read` through a compatible host. See [account, host and privacy prerequisites](skills/outreachgenie-list-audit/references/setup.md) before connecting. The local script makes no network calls, but the host/model provider processes records returned through MCP.

The package uses the [Agent Skills format](https://agentskills.io/specification). Install the `skills/outreachgenie-list-audit` folder into a skill directory supported by your host. Current [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) lists `~/.agents/skills` for user skills and `.agents/skills` within a repository. Keep the directory name and review an existing installation before replacing it. This is a local skill package, not a published plugin.

The offline helper and fictional fixture have been validated. One explicit native Codex CLI 0.160.0 invocation also passed on Linux with Python 3.11.8 in an isolated workspace. This verifies the fictional fixture workflow only; hosted OAuth, real-workspace capture, automatic skill selection, Claude Code and ChatGPT/Claude web execution remain unverified. See the [compatibility evidence](skills/outreachgenie-list-audit/references/setup.md#compatibility-evidence). A browser-only host without local Python cannot run the helper as written.

## How it differs from scraper-based LinkedIn MCP servers

Many open-source LinkedIn MCP servers sign in to LinkedIn with your session and
read pages on demand. This MCP server does not browse LinkedIn directly. It gives
the agent an [OutreachGenie](https://www.outreachgenie.ai) workspace with lists, notes,
flows, and campaign state. LinkedIn-side steps (invitations, messages, visits)
run later through the OutreachGenie Chrome companion in your own browser, at
the pace your workspace limits allow.

Importing Sales Navigator search results is a separate, user-initiated Chrome
companion workflow in your browser. Save the people to a workspace list first;
MCP can then work with those saved records. The MCP server does not browse Sales
Navigator or extract its search results. See the [Sales Navigator import and CSV
export guide](https://www.outreachgenie.ai/blog/export-sales-navigator-leads-to-csv)
for the browser steps, import limits and separate Sales Navigator subscription.

## Setup

Prefer OAuth when your host supports hosted MCP authorization. For the saved-list audit, grant only `crm.read`; it needs no write or activation scopes. The API-key examples below are fallback configuration and may grant broader access. A skill's read-tool instructions do not reduce an API key's server permissions.

### Claude (web and desktop) and ChatGPT — OAuth

1. Click **Add to Claude** above, or go to Settings → Connectors → Add custom connector and paste the server URL.
2. Sign in to OutreachGenie, choose a workspace, and approve only the scopes you want.
3. Ask: _"Verify my OutreachGenie workspace and tell me which tools you can use."_

In ChatGPT, add the same URL as a connector where your plan allows custom connectors.

### Claude Code — API key

Create a key in OutreachGenie under Settings → API keys, store it in `LINKEDIN_CRM_API_KEY`, then:

```bash
claude mcp add --transport http linkedin-crm \
  https://api.outreachgenie.ai/mcp \
  --header "Authorization: Bearer $LINKEDIN_CRM_API_KEY"
```

### Codex

```toml
[mcp_servers.linkedin-crm]
url = "https://api.outreachgenie.ai/mcp"
bearer_token_env_var = "LINKEDIN_CRM_API_KEY"
```

## Available tools

The table below gives examples. Ask the connected client for its current tool inventory and granted scopes; available tools can change. Saved-list audits additionally use `get_workspace_context`, `get_prospect_list` and `list_prospects_in_list`, all within `crm.read`.

| Area      | Tools                                                                                                                                        | Scope                                   |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Workspace | `verify_runtime_auth`                                                                                                                        | `crm.read`                              |
| Prospects | `lookup_prospect_by_linkedin_url`, `import_prospect`, `batch_import_prospects_to_list`, `update_prospect_note`, `add_prospect_to_list`       | `crm.read`, `crm.write`                 |
| Lists     | `list_prospect_lists`, `create_prospect_list`                                                                                                | `crm.read`, `crm.write`                 |
| Flows     | `list_flows`, `get_flow`, `create_flow`, `list_flow_template_fields`                                                                         | `crm.read`, `crm.write`                 |
| Campaigns | `create_campaign_draft`, `create_runtime_campaign`, `activate_campaign`                                                                      | `campaigns.write`, `campaigns.activate` |
| Content   | `create_content_draft`, `get_content_draft`, `update_content_draft`, `list_content_drafts`, `list_content_calendar`, `get_content_analytics` | `content.*`                             |

Leave `campaigns.activate` out if you want the agent to prepare campaigns but never start them.

## Example prompts

- "Create a list called Conference leads, import these LinkedIn profile URLs, and tell me which records were created or already existed."
- "Look up this LinkedIn profile URL and summarize what we already know before I write to them."
- "Use the Partner outreach flow with the Partner leads list. Summarize the launch plan and wait for my approval before creating the campaign."

## Limits and policy

MCP access has no separate API or MCP charge. Free includes 80 outreach actions
per week and 500 new prospects per week from LinkedIn search, Sales Navigator
and post engagement. Pro costs $15/month or $150/year (USD) and removes those
weekly product quotas. LinkedIn's own restrictions and workspace execution
controls still apply. See [current pricing and plan allowances](https://www.outreachgenie.ai/pricing)
for the full breakdown.

LinkedIn says third-party software that automates activity on its website is
not allowed, and accounts may be restricted. An AI client doesn't change that.
Keep batches small enough to review and stop on any warning.
OutreachGenie is independent and not affiliated with LinkedIn.

## License

Documentation and the audit skill in this repository are MIT licensed. The hosted service is
governed by the [OutreachGenie terms](https://www.outreachgenie.ai/terms).
