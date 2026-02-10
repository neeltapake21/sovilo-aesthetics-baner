# start-all.ps1 - launch backend and frontend in separate PowerShell windows
# Run from the repository root: powershell -ExecutionPolicy Bypass -File .\start-all.ps1

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList @(
    '-NoExit',
    '-Command',
    "Set-Location -Path '$root\\backend'; if (Test-Path .venv\\Scripts\\Activate.ps1) { . .venv\\Scripts\\Activate.ps1 }; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
)

# Start frontend in a new PowerShell window (install deps if node_modules missing)
$frontendCmd = "Set-Location -Path '$root\\frontend'; if (!(Test-Path node_modules)) { npm install }; npm run dev"
Start-Process powershell -ArgumentList @('-NoExit','-Command',$frontendCmd)
