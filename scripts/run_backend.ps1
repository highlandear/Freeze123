$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$CondaPython = "C:\anaconda3\python.exe"

if (Test-Path $VenvPython) {
  & $VenvPython -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
}
elseif (Test-Path $CondaPython) {
  & $CondaPython -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
}
else {
  python -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
}
