from pathlib import Path
root = Path(r'D:\\codexWorkspace\\ApiMapMCPServer\\ai-dev-os\\examples')
print('exists', root.exists())
print('files', [str(p) for p in root.rglob('*.json')])
