"use client";

import React, { useMemo, useState } from "react";
import { streamAgent } from "@ai-dev-os/sdk";
import { TraceStore } from "@ai-dev-os/devtools";

export default function Page() {
  const [message, setMessage] = useState("tool:text_to_image {\"prompt\": \"a neon tiger\"}");
  const [events, setEvents] = useState<string[]>([]);
  const trace = useMemo(() => new TraceStore(), []);

  const run = () => {
    setEvents([]);
    trace.clear();
    streamAgent("http://localhost:8000", { message }, (evt) => {
      trace.add({ type: evt.event as any, timestamp: Date.now(), payload: evt.data });
      setEvents((prev) => [...prev, `${evt.event}: ${evt.data}`]);
    });
  };

  return (
    <div style={{ padding: 24, fontFamily: "ui-sans-serif" }}>
      <h1 style={{ fontSize: 22, fontWeight: 700 }}>Playground</h1>
      <p style={{ color: "#475569" }}>Streaming MCP agent output + tool call trace.</p>
      <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
        <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={4} style={{ padding: 10, border: "1px solid #e2e8f0" }} />
        <button onClick={run} style={{ padding: 10, background: "#111827", color: "white", borderRadius: 8 }}>Run</button>
      </div>
      <div style={{ marginTop: 16, background: "#f8fafc", padding: 12, borderRadius: 8 }}>
        {events.map((e, i) => (
          <div key={i} style={{ fontFamily: "monospace", fontSize: 12 }}>{e}</div>
        ))}
      </div>
    </div>
  );
}
