import webbrowser

def open_url_in_default_browser(url):
    try:
        webbrowser.open(url, new=2)  # new=2: open in a new tab, if possible
    except Exception as e:
        print(f"Failed to open URL {url} in the default browser: {e}")

# Example usage
open_url_in_default_browser("https://www.example.com")