"use client";

import React, { useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MiniMap, Node, Edge } from "reactflow";
import "reactflow/dist/style.css";
import { A2UIRenderer } from "@ai-dev-os/a2ui-renderer";
import { streamAgent, invokeTool } from "@ai-dev-os/sdk";
import { TraceStore } from "@ai-dev-os/devtools";

const initialNodes: Node[] = [
  { id: "1", position: { x: 0, y: 0 }, data: { label: "User" }, type: "input" },
  { id: "2", position: { x: 200, y: 0 }, data: { label: "Agent" } },
  { id: "3", position: { x: 420, y: 0 }, data: { label: "Tool" } },
];
const initialEdges: Edge[] = [
  { id: "e1-2", source: "1", target: "2" },
  { id: "e2-3", source: "2", target: "3" },
];

export default function Page() {
  const [tab, setTab] = useState("playground");
  const [message, setMessage] = useState("tool:text_to_image {\"prompt\": \"a neon tiger\"}");
  const [events, setEvents] = useState<string[]>([]);
  const [toolConfig, setToolConfig] = useState(`{
  "name": "text_to_image",
  "version": "0.1.0",
  "description": "Generate image from text",
  "auth": { "type": "none" },
  "request": {
    "method": "POST",
    "url": "http://localhost:9001/generate",
    "headers": { "Content-Type": "application/json" },
    "body": { "prompt": "{{input.prompt}}" }
  },
  "input_schema": {
    "type": "object",
    "properties": { "prompt": { "type": "string" } },
    "required": ["prompt"]
  },
  "output_mapping": { "image_url": "$.image_url", "prompt": "$.prompt" }
}`);

  const trace = useMemo(() => new TraceStore(), []);
  const [a2ui, setA2ui] = useState<any>({ type: "markdown", data: "Ready." });

  const run = () => {
    setEvents([]);
    trace.clear();
    streamAgent("http://localhost:8000", { message }, (evt) => {
      trace.add({ type: evt.event as any, timestamp: Date.now(), payload: evt.data });
      setEvents((prev) => [...prev, `${evt.event}: ${evt.data}`]);
    });
  };

  const testTool = async () => {
    const cfg = JSON.parse(toolConfig);
    const res = await invokeTool("http://localhost:8000", { tool_name: cfg.name, inputs: { prompt: "a neon tiger" } });
    setA2ui({ type: "code", data: JSON.stringify(res, null, 2) });
  };

  return (
    <div style={{ padding: 24, fontFamily: "ui-sans-serif" }}>
      <h1 style={{ fontSize: 24, fontWeight: 800 }}>Agent IDE</h1>
      <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
        {[
          ["playground", "Playground"],
          ["mcp", "MCP Builder"],
          ["agent", "Agent Builder"],
          ["devtools", "DevTools"],
        ].map(([k, label]) => (
          <button key={k} onClick={() => setTab(k)} style={{ padding: "6px 10px", borderRadius: 8, background: tab === k ? "#0f172a" : "#e2e8f0", color: tab === k ? "#fff" : "#0f172a" }}>
            {label}
          </button>
        ))}
      </div>

      {tab === "playground" && (
        <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
          <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={4} style={{ padding: 10, border: "1px solid #e2e8f0" }} />
          <button onClick={run} style={{ padding: 10, background: "#111827", color: "white", borderRadius: 8 }}>Run</button>
          <div style={{ background: "#f8fafc", padding: 12, borderRadius: 8 }}>
            {events.map((e, i) => (
              <div key={i} style={{ fontFamily: "monospace", fontSize: 12 }}>{e}</div>
            ))}
          </div>
        </div>
      )}

      {tab === "mcp" && (
        <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
          <textarea value={toolConfig} onChange={(e) => setToolConfig(e.target.value)} rows={18} style={{ padding: 10, border: "1px solid #e2e8f0", fontFamily: "monospace" }} />
          <button onClick={testTool} style={{ padding: 10, background: "#111827", color: "white", borderRadius: 8 }}>Test Tool</button>
          <A2UIRenderer payload={a2ui} />
        </div>
      )}

      {tab === "agent" && (
        <div style={{ marginTop: 16, height: 300, border: "1px solid #e2e8f0", borderRadius: 8 }}>
          <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </div>
      )}

      {tab === "devtools" && (
        <div style={{ marginTop: 16 }}>
          <h3>Trace Timeline</h3>
          <ul>
            {trace.list().map((t, i) => (
              <li key={i}>{new Date(t.timestamp).toLocaleTimeString()} - {t.type}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
