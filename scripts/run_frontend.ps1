$ErrorActionPreference = "Stop"

Push-Location "$PSScriptRoot\..\src\frontend"
try {
  if (-not (Test-Path "node_modules")) {
    Write-Host "Frontend dependencies are missing. Run: npm install"
    exit 1
  }

  npm run dev
}
finally {
  Pop-Location
}
