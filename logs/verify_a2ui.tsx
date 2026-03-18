import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { A2UIRenderer } from "../packages/a2ui-renderer/src/index";

const cases = [
  { name: "markdown", payload: { type: "markdown", data: "# Hello" } },
  { name: "code", payload: { type: "code", data: "print('ok')" } },
  { name: "table", payload: { type: "table", data: [{ a: 1, b: 2 }] } },
  { name: "form", payload: { type: "form", data: [{ name: "q", label: "Question" }] } },
  { name: "chart", payload: { type: "chart", data: [1, 2, 3] } },
];

for (const c of cases) {
  const html = renderToStaticMarkup(React.createElement(A2UIRenderer as any, { payload: c.payload }));
  console.log(`CASE:${c.name}`);
  console.log(html);
}
