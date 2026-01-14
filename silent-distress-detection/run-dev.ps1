# PowerShell helper to start backend, edge agent, and frontend in separate windows (Windows)
$root = (Resolve-Path .).Path

# Backend window: create venv if missing and start uvicorn
Start-Process powershell -ArgumentList "-NoExit -Command cd '$root'; if (-not (Test-Path .\\backend\\venv)) { cd .\\backend; python -m venv venv; pip install -r requirements.txt; cd '$root' }; .\\backend\\venv\\Scripts\\Activate; uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000"

# Edge agent window: activate venv and run edge agent as a module
Start-Process powershell -ArgumentList "-NoExit -Command cd '$root'; .\\backend\\venv\\Scripts\\Activate; python -m backend.edge_agent"

# Frontend window: install if needed and start
Start-Process powershell -ArgumentList "-NoExit -Command cd '$root\\frontend'; if (-not (Test-Path .\\node_modules)) { npm install }; npm start"

Write-Host "Started backend, edge agent, and frontend in new PowerShell windows (check each window for logs)."