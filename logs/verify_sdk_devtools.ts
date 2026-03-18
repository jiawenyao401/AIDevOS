import { invokeTool, streamAgent } from "../packages/sdk/src/index";
import { TraceStore } from "../packages/devtools/src/index";

process.on("unhandledRejection", (err: any) => {
  if (err?.name === "AbortError") {
    console.log("ABORT_OK", true);
    return;
  }
  console.error(err);
  process.exit(1);
});

process.on("uncaughtException", (err: any) => {
  if (err?.name === "AbortError") {
    console.log("ABORT_OK", true);
    return;
  }
  console.error(err);
  process.exit(1);
});

async function run() {
  const trace = new TraceStore();

  const invokeRes = await invokeTool("http://localhost:8000", {
    tool_name: "text_to_image",
    inputs: { prompt: "sdk invoke" },
  });
  trace.add({ type: "result", timestamp: Date.now(), payload: invokeRes });

  const events: any[] = [];
  await new Promise<void>((resolve) => {
    const stop = streamAgent(
      "http://localhost:8000",
      { message: 'tool:text_to_image {"prompt": "sdk stream"}' },
      (evt) => {
        events.push(evt);
        trace.add({ type: evt.event as any, timestamp: Date.now(), payload: evt.data });
        if (evt.event === "result") {
          stop();
          resolve();
        }
      }
    );
  });

  console.log("INVOKE_OK", invokeRes?.ok === true);
  console.log("STREAM_EVENTS", events.map((e) => e.event));
  console.log("TRACE_COUNT", trace.list().length);
}

run().catch((e) => {
  if (e?.name === "AbortError") {
    console.log("ABORT_OK", true);
    process.exit(0);
  }
  console.error(e);
  process.exit(1);
});
