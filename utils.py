import os
def ensure_asset_directories():
    """Create the asset directories used by the application."""
    os.makedirs("assets/photos", exist_ok=True)
    os.makedirs("assets/icons", exist_ok=True)
