"""
OneHealth Nexus - Unified Analysis Runner
Coordinates execution of Temporal Analysis, Spatial Biodiversity Intelligence,
and Emerging Signal Detection.
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def run_script(script_name: str):
    script_path = ROOT / script_name
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run([sys.executable, str(script_path)], check=True)
    return result.returncode

def main():
    print("=" * 60)
    print(" ONEHEALTH NEXUS - UNIFIED ANALYTICAL PIPELINE")
    print("=" * 60)
    
    scripts = [
        "temporal_analysis.py",
        "spatial_analysis.py",
        "emerging_signals.py"
    ]
    
    for s in scripts:
        run_script(s)
        
    print("\n" + "=" * 60)
    print(" ALL ANALYTICAL MODULES SUCCESSFULLY EXECUTED")
    print(" Outputs generated:")
    print("  - analysis/temporal_summary.csv & temporal_trend.png")
    print("  - analysis/spatial_summary.csv & spatial_distribution.png")
    print("  - analysis/emerging_signals.csv")
    print("=" * 60)

if __name__ == "__main__":
    main()
