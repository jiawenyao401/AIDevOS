import sys
from pathlib import Path
sys.path.insert(0, str(Path(r'D:\\codexWorkspace\\ApiMapMCPServer\\ai-dev-os\\services\\tool-hub')))
from registry import ToolRegistry
root = str(Path(r'D:\\codexWorkspace\\ApiMapMCPServer\\ai-dev-os\\examples'))
reg = ToolRegistry(root)
reg.load()
print([t.name for t in reg.list_tools()])
