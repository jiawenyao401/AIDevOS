export type ToolCallPayload = { tool_name: string; inputs: Record<string, any>; version?: string };

export async function listTools(baseUrl: string) {
  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/tools`);
  return await res.json();
}

export async function invokeTool(baseUrl: string, payload: ToolCallPayload) {
  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/invoke`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return await res.json();
}

export function streamAgent(baseUrl: string, payload: any, onEvent: (evt: { event: string; data: string }) => void) {
  const url = `${baseUrl.replace(/\/$/, "")}/stream`;
  const controller = new AbortController();
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: controller.signal,
  }).then(async (res) => {
    const reader = res.body?.getReader();
    if (!reader) return;
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";
      for (const part of parts) {
        const lines = part.split("\n");
        const eventLine = lines.find((l) => l.startsWith("event:"));
        const dataLine = lines.find((l) => l.startsWith("data:"));
        if (eventLine && dataLine) {
          onEvent({ event: eventLine.replace("event:", "").trim(), data: dataLine.replace("data:", "").trim() });
        }
      }
    }
  });
  return () => controller.abort();
}
