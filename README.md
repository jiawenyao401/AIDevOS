🚀 AI Dev OS
Build AI Agents like you build apps.
Turn any API into an AI-capable tool in 30 seconds. Build, debug, and deploy AI agents — without writing glue code.

✨ What is this?
AI Dev OS is a next-generation development platform for building AI systems.

It combines:

🧠 MCP OS — Standardized tool + agent runtime
🔌 API2MCP Engine — Convert any API into an AI tool
🎨 A2UI — Agents render UI, not just text
💻 Agent IDE — Build & debug agents visually
⚡ Why this matters
Today:

APIs are hard to integrate into AI agents
Tools are not standardized
Debugging AI systems is painful
UI is disconnected from agents
AI Dev OS fixes all of this.

🔥 Key Features
1. Turn ANY API into an AI Tool
{
  "name": "text_to_image",
  "request": {
    "url": "https://api.example.com/generate",
    "method": "POST"
  },
  "input_schema": {
    "prompt": "string"
  }
}
➡️ Now your agent can call it automatically.

2. Visual Agent Builder
Drag & drop workflows
ReAct / Multi-Agent
Tool orchestration
3. Built-in DevTools (like Chrome DevTools for AI)
Trace every step
Inspect tool calls
Replay runs
4. Agents render UI (A2UI)
Instead of:

"Here is your data..."
You get:

📊 Tables
📈 Charts
🧾 Forms
5. Streaming-first architecture
Token streaming
Tool call streaming
Real-time UI updates
🧠 Architecture
Agent IDE (UI)
      ↓
MCP OS (Runtime)
      ↓
Any API / DB / Service
🚀 Quick Start
git clone https://github.com/yourname/ai-dev-os
cd ai-dev-os

# backend
cd services/mcp-gateway
pip install -r requirements.txt
uvicorn main:app --reload

# frontend
cd apps/web-ide
npm install
npm run dev
🧪 Example: Build a Text-to-Image Agent
Add API config
Create Agent
Ask:
Generate a cyberpunk city image
➡️ Agent calls API → returns image → renders UI

🧩 Project Structure
ai-dev-os/
├── apps/
│   ├── web-ide/
│   ├── playground/
├── services/
│   ├── api2mcp-engine/
│   ├── mcp-gateway/
│   ├── agent-runtime/
├── packages/
│   ├── a2ui-renderer/
🛠 Use Cases
AI SaaS builders
Internal copilots
Automation platforms
Multi-agent systems
💡 Vision
APIs were for developers. MCP tools are for AI.

We believe:

👉 Every API will become AI-callable 👉 Every app will be an agent

🤝 Contributing
PRs welcome. We are building the AI infrastructure layer for the next decade.


⭐ Star this repo
If this clicks for you, give it a ⭐ It helps more than you think.
