import os

def check_downloaded_google_sheet_data(g_sheets_file) -> bool:
    return os.path.exists(g_sheets_file)