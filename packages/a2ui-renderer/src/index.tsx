import React from "react";
import ReactMarkdown from "react-markdown";

type A2UIData = {
  type: "table" | "chart" | "markdown" | "code" | "form";
  data: any;
};

type Props = {
  payload: A2UIData;
  onSubmit?: (values: Record<string, any>) => void;
};

export function A2UIRenderer({ payload, onSubmit }: Props) {
  if (!payload) return null;

  if (payload.type === "markdown") {
    return <ReactMarkdown>{String(payload.data ?? "")}</ReactMarkdown>;
  }

  if (payload.type === "code") {
    return (
      <pre style={{ background: "#0f172a", color: "#e2e8f0", padding: 16, borderRadius: 8 }}>
        <code>{String(payload.data ?? "")}</code>
      </pre>
    );
  }

  if (payload.type === "table") {
    const rows = Array.isArray(payload.data) ? payload.data : [];
    const headers = rows.length > 0 ? Object.keys(rows[0]) : [];
    return (
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h} style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0", padding: 8 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {headers.map((h) => (
                <td key={h} style={{ padding: 8, borderBottom: "1px solid #f1f5f9" }}>{String(row[h] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  if (payload.type === "form") {
    const fields = Array.isArray(payload.data) ? payload.data : [];
    return (
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget);
          const values: Record<string, any> = {};
          data.forEach((v, k) => (values[k] = v));
          onSubmit?.(values);
        }}
        style={{ display: "grid", gap: 12 }}
      >
        {fields.map((f: any) => (
          <label key={f.name} style={{ display: "grid", gap: 6 }}>
            <span>{f.label ?? f.name}</span>
            <input name={f.name} defaultValue={f.default ?? ""} style={{ padding: 8, border: "1px solid #e2e8f0", borderRadius: 6 }} />
          </label>
        ))}
        <button type="submit" style={{ padding: 10, borderRadius: 8, background: "#111827", color: "#fff" }}>Submit</button>
      </form>
    );
  }

  if (payload.type === "chart") {
    return (
      <div style={{ padding: 16, background: "#f8fafc", borderRadius: 8 }}>
        Chart placeholder (data points: {Array.isArray(payload.data) ? payload.data.length : 0})
      </div>
    );
  }

  return null;
}
