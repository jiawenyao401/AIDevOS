import json
from pathlib import Path
p = Path(r'D:\\codexWorkspace\\ApiMapMCPServer\\ai-dev-os\\examples\\text-to-image-tool\\config.json')
print(json.loads(p.read_text(encoding='utf-8')).get('name'))
