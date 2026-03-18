# Verification Summary - 2026-03-18

## Services Startup
- mock API (text-to-image) started via `uvicorn mock_server:app --port 9001`
- MCP gateway started on port 8000
- Tool hub started on port 8002

## Health Checks
- http://localhost:9001/health -> OK
- http://localhost:8000/health -> OK
- http://localhost:8002/health -> OK

## Tool Discovery
- http://localhost:8000/tools -> discovered tools: `support_agent`, `text_to_image`

## End-to-End Tool Invocation
Request:
- POST http://localhost:8000/invoke
- body: {"tool_name":"text_to_image","inputs":{"prompt":"a neon tiger"}}

Result:
- ok: true
- data: image_url, prompt, seed
- status_code: 200
- latency_ms: ~834

## Fixes Applied During Verification
- Read tool configs with `utf-8-sig` to handle BOM in JSON
- Disabled proxy inheritance for httpx (`trust_env=False`) to avoid 502 on localhost

## SSE /stream Verification
Request:
- POST http://localhost:8000/stream
- message: tool:text_to_image {"prompt": "sse neon tiger"}

Observed events:
- token (multiple)
- tool_call (text_to_image)
- result (ok: true, status_code: 200)

Result sample:
- image_url: https://images.example.com/2879.png
- prompt: sse neon tiger
- seed: 2879
- latency_ms: ~613

Notes:
- Client used `trust_env=False` to avoid proxy interference on localhost.

## Agent Runtime Verification
Health:
- http://localhost:8003/health -> OK

/run:
- POST http://localhost:8003/run
- message: tool:text_to_image {"prompt": "agent runtime"}
- tool_endpoint: http://localhost:8000
- result: ok true, tool call succeeded

/stream:
- POST http://localhost:8003/stream
- message: tool:text_to_image {"prompt": "agent runtime stream"}
- events: token, tool_call, result
- result: ok true, status_code 200

Notes:
- agent-runtime now uses httpx `trust_env=False` to avoid proxy issues on localhost.

## Memory Hub Verification
Health:
- http://localhost:8004/health -> OK

Session set/get:
- POST /memory/session-1 with 2 items
- GET /memory/session-1 returned 2 items

Append:
- POST /memory/session-1/append
- GET /memory/session-1 returned 3 items

Notes:
- Redis required and assumed running on localhost:6379

## UI Verification
Setup:
- npm install at repo root completed
- Next.js dev servers started via npm.cmd
  - web-ide: http://localhost:3000
  - playground: http://localhost:3001

Server readiness:
- Logs show "Ready" for both apps
- HTTP HEAD check:
  - http://localhost:3000 -> 200 OK (Next.js)
  - http://localhost:3001 -> 200 OK (Next.js)

UI rendering:
- web-ide HTML contains heading "Agent IDE"
- playground HTML fetch was not captured (GET timing out), but server is listening and responds to HEAD

Notes:
- npm logged ENOWORKSPACES warnings, but Next dev servers still reached "Ready"

## A2UI Renderer Verification
Runtime render (ReactDOMServer via tsx):
- markdown -> <h1>Hello</h1>
- code -> <pre><code>...</code></pre>
- table -> <table> with headers a,b and row 1,2
- form -> <form> with input name=q and Submit button
- chart -> placeholder div with data point count

## Web IDE UI Verification (HTTP)
- http://localhost:3000 HTML contains headings:
  - Agent IDE
  - MCP Builder
  - Agent Builder
  - DevTools

## Playground UI Verification (HTTP)
- http://localhost:3001 HTML contains heading:
  - Playground

## MCP Builder / DevTools Verification (SDK Simulation)
- SDK invokeTool -> ok true (text_to_image)
- SDK streamAgent -> events: token, tool_call, result
- DevTools TraceStore -> captured 7 events

Notes:
- streamAgent abort is expected on client stop; treated as OK (AbortError handled)

## API2MCP Engine Direct Verification
- Service: http://localhost:8005
- /invoke success with mock API -> ok true, data mapped (seed/prompt/image_url)
- /invoke failure with bad URL -> ok false (error path exercised)

Notes:
- Fixed relative imports in api2mcp-engine for uvicorn direct execution

## Tool Hub Config Retrieval
- GET http://localhost:8002/tools/text_to_image -> 200 with config payload

## Memory Hub Edge Cases
- GET /memory/does-not-exist -> items: []
- POST /memory/new-session/append -> size 1
- GET /memory/new-session -> 1 item

## UI Click Verification (Playwright)
- Headless Chromium automated click path
- Web IDE: Playground -> MCP Builder -> Agent Builder -> DevTools
  - Verified presence of: textarea + Run, Test Tool button, React Flow canvas, Trace Timeline
- Playground: verified Playground heading, textarea, Run button

Result:
- WEB_IDE_OK true
- PLAYGROUND_OK true
