# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Your Password", #enter your mysql password
    "database": "Institute Management"
}

# SMTP Configuration for Email
SMTP_CONFIG = {
    "host": "ims.gmail.com",
    "port": 587,
    "user": "", #enter your email
    "password": "" #enter your app password
}


# Color Scheme
COLORS = {
    "primary": "#1f538d",
    "secondary": "#14a085",
    "success": "#27ae60",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db",
    "dark": "#105ca9",
    "light": "#ecf0f1",
    "sidebar": "#1d78bd",
    "sidebar_hover": "#A98914" 
}

# Paths
ASSETS_PATH = "assets"
PHOTOS_PATH = "assets/photos"
ICONS_PATH = "assets/icons"

COLORS.update({
    "card_blue": "#3B82F6",
    "card_green": "#22C55E",
    "card_orange": "#F59E0B",
    "card_teal": "#14B8A6",
})