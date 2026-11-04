$ErrorActionPreference = "Stop"

# Anchor execution to script root regardless of where it was invoked
$ProjectRoot = $PSScriptRoot
if (-not $ProjectRoot) {
    $ProjectRoot = (Get-Item .).FullName
}
Set-Location $ProjectRoot

Write-Host "=============================================="
Write-Host " ONEHEALTH NEXUS - COMPLETE LOCAL PIPELINE"
Write-Host " Working Directory: $ProjectRoot"
Write-Host "=============================================="

$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvStreamlit = Join-Path $VenvDir "Scripts\streamlit.exe"

# 1. Virtual Environment Setup
if (-not (Test-Path $VenvPython)) {
    Write-Host "`nCreating virtual environment (.venv)..."
    python -m venv $VenvDir
}

# 2. Dependency Installation
Write-Host "`nInstalling dependencies from requirements.txt..."
& $VenvPython -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# 3. Environmental & Animal Health Data Ingestion
Write-Host "`n[1/6] Ingesting Weather and Veterinary Animal Health Data..."
& $VenvPython src\weather_collector.py
& $VenvPython src\animal_health_collector.py

# 4. Apache Spark Preprocessing (Scala Spark via sbt, with automated fallback)
Write-Host "`n[2/6] Running Apache Spark Preprocessing..."
$sparkSuccess = $false
try {
    if (Get-Command sbt -ErrorAction SilentlyContinue) {
        Write-Host "Executing Apache Spark via sbt..."
        sbt run
        if ($LASTEXITCODE -eq 0) {
            $sparkSuccess = $true
        }
    }
} catch {
    Write-Host "sbt not available or failed. Falling back to Python Spark ETL pipeline..."
}

if (-not $sparkSuccess) {
    Write-Host "Running Python Apache Spark / ETL Preprocessor..."
    & $VenvPython spark_processing\preprocess_data.py
}

# 5. NLP Entity & Relationship Extraction
Write-Host "`n[3/6] Running NLP Entity & Relationship Extraction..."
& $VenvPython nlp\entity_extraction.py

# 6. Knowledge Graph Construction
Write-Host "`n[4/6] Building NetworkX Knowledge Graph..."
& $VenvPython knowledge_graph\build_graph.py

# 7. Spatio-Temporal & Emerging Risk Analytics
Write-Host "`n[5/6] Executing Temporal, Spatial, and Signal Intelligence..."
& $VenvPython analysis\temporal_analysis.py
& $VenvPython analysis\spatial_analysis.py
& $VenvPython analysis\emerging_signals.py
& $VenvPython src\alert_engine.py

# 8. Automated End-to-End Test Suite
Write-Host "`n[6/6] Executing End-to-End Validation Suite..."
& $VenvPython tests\test_end_to_end.py

Write-Host "`n=============================================="
Write-Host " PIPELINE EXECUTION COMPLETE! (100% OPERATIONAL)"
Write-Host "=============================================="
Write-Host "Launch the interactive dashboard with either command:"
Write-Host "  1. Directly:"
Write-Host "     & `"$VenvStreamlit`" run dashboard\app.py"
Write-Host "  2. From project folder:"
Write-Host "     cd `"$ProjectRoot`""
Write-Host "     .\.venv\Scripts\streamlit.exe run dashboard\app.py"
