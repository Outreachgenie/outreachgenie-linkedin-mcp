# LinkedIn MCP server for Claude and ChatGPT — OutreachGenie

Connect Claude, ChatGPT, Claude Code, or Codex to your LinkedIn prospecting
workspace: look up and import prospects, organize lists, build outreach flows,
and prepare campaigns from chat. Hosted, OAuth-secured, and free.

```
https://api.outreachgenie.ai/mcp
```

**[Add to Claude](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=OutreachGenie&connectorUrl=https%3A%2F%2Fapi.outreachgenie.ai%2Fmcp)** · [Website](https://www.outreachgenie.ai/linkedin-mcp) · [Developer docs](https://www.outreachgenie.ai/developers)

## How it differs from scraper-based LinkedIn MCP servers

Many open-source LinkedIn MCP servers sign in to LinkedIn with your session and
read pages on demand. This one doesn't touch LinkedIn at all. It gives the agent
an [OutreachGenie](https://www.outreachgenie.ai) workspace with lists, notes,
flows, and campaign state. LinkedIn-side steps (invitations, messages, visits)
run later through the OutreachGenie Chrome companion in your own browser, at
the pace your workspace limits allow.

## Setup

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

## Tools (21)

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

LinkedIn says third-party software that automates activity on its website is
not allowed, and accounts may be restricted. An AI client doesn't change that.
Keep batches small enough to review and stop on any warning.
OutreachGenie is independent and not affiliated with LinkedIn.

## License

Documentation in this repository is MIT licensed. The hosted service is
governed by the [OutreachGenie terms](https://www.outreachgenie.ai/terms).
