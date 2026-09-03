# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # enter your MySQL password
    "database": "Institute Management"
}

# SMTP Configuration for Email
SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "",  # enter your email
    "password": ""  # enter your app password
}

# Color Scheme
COLORS = {
    "primary": "#2563EB",       # Main blue
    "secondary": "#1D4ED8",     # Dark blue
    "success": "#16A34A",       # Green
    "danger": "#DC2626",        # Red
    "warning": "#D97706",       # Orange
    "info": "#3B82F6",          # Light blue
    "dark": "#1E3A8A",          # Navy
    "light": "#F8FAFC",         # Very light background
    "sidebar": "#1E3A8A",       # Navy sidebar
    "sidebar_hover": "#2563EB", # Blue hover

    # Dashboard cards
    "card_blue": "#3B82F6",
    "card_green": "#22C55E",
    "card_orange": "#F59E0B",
    "card_teal": "#0EA5E9",
}

COLORS.update({
    "card_blue": "#3B82F6",
    "card_green": "#22C55E",
    "card_orange": "#F59E0B",
    "card_teal": "#14B8A6",
})

# Paths
ASSETS_PATH = "assets"
PHOTOS_PATH = "assets/photos"
ICONS_PATH = "assets/icons"
