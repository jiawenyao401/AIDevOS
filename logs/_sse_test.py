import httpx

url = 'http://localhost:8000/stream'
payload = {'message': 'tool:text_to_image {"prompt": "sse neon tiger"}'}

with httpx.stream('POST', url, json=payload, timeout=10.0, trust_env=False) as r:
    r.raise_for_status()
    events = []
    buf = ''
    for line in r.iter_lines():
        if line is None:
            continue
        line = line.strip()
        if not line:
            if buf:
                events.append(buf)
                buf = ''
            if len(events) >= 12:
                break
            continue
        buf += line + '\n'

print('\n---EVENTS---\n')
for e in events:
    print(e)
