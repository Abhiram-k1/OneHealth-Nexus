"""
OneHealth Nexus — Root Deployment Entrypoint for Streamlit Community Cloud
"""
import os
import runpy

# Ensure repository root is in sys.path and set as working directory
root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

# Execute dashboard/app.py
target_script = os.path.join(root_dir, "dashboard", "app.py")
runpy.run_path(target_script, run_name="__main__")
