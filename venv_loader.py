import sys
import os

def activate_venv():
    """Dynamically adds the virtual environment's site-packages to sys.path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, ".venv")

    # Determine the correct site-packages path
    if os.name == "nt":  # Windows
        site_packages = os.path.join(venv_path, "Lib", "site-packages")
    else:  # Linux/macOS
        site_packages = os.path.join(venv_path, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")

    # Add site-packages to sys.path
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)
    else:
        print("Warning: site-packages directory not found!", file=sys.stderr)
        exit
