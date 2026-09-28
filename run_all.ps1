$ErrorActionPreference = "Stop"

Write-Host "=============================================="
Write-Host " ONEHEALTH NEXUS - COMPLETE LOCAL PIPELINE"
Write-Host "=============================================="

if (-not (Test-Path ".venv")) {
    Write-Host "`nCreating virtual environment (.venv)..."
    python -m venv .venv
}

Write-Host "`nInstalling dependencies..."
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" -m spacy download en_core_web_sm

Write-Host "`n[1/4] Running Scala + Apache Spark Preprocessing..."
sbt run

Write-Host "`n[2/4] Running NLP Entity & Relationship Extraction..."
& ".\.venv\Scripts\python.exe" nlp\entity_extraction.py

Write-Host "`n[3/4] Building NetworkX Knowledge Graph..."
& ".\.venv\Scripts\python.exe" knowledge_graph\build_graph.py

Write-Host "`n[4/4] Executing Temporal, Spatial, and Signal Intelligence..."
& ".\.venv\Scripts\python.exe" analysis\temporal_analysis.py
& ".\.venv\Scripts\python.exe" analysis\spatial_analysis.py
& ".\.venv\Scripts\python.exe" analysis\emerging_signals.py

Write-Host "`n=============================================="
Write-Host " PIPELINE EXECUTION COMPLETE!"
Write-Host "=============================================="
Write-Host "Launch the interactive dashboard with:"
Write-Host ".\.venv\Scripts\streamlit.exe run dashboard\app.py"
