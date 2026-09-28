$ProjectRoot = $PSScriptRoot
if (-not $ProjectRoot) {
    $ProjectRoot = (Get-Item .).FullName
}
Set-Location $ProjectRoot

$VenvStreamlit = Join-Path $ProjectRoot ".venv\Scripts\streamlit.exe"

if (-not (Test-Path $VenvStreamlit)) {
    Write-Host "Virtual environment not detected. Running initial pipeline setup..."
    & (Join-Path $ProjectRoot "run_all.ps1")
}

Write-Host "Starting OneHealth Nexus Command Center..."
& $VenvStreamlit run dashboard\app.py
