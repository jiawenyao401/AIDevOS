export type TraceEvent = {
  type: "token" | "tool_call" | "result";
  timestamp: number;
  payload: any;
};

export class TraceStore {
  private events: TraceEvent[] = [];
  add(event: TraceEvent) {
    this.events.push(event);
  }
  list() {
    return [...this.events];
  }
  clear() {
    this.events = [];
  }
}
