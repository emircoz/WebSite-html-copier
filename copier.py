import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

def get_valid_filename(url):
    """Generate a safe filename from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '').split('.')[0]
    domain = "".join(c for c in domain if c.isalnum() or c in ('-', '_'))
    return f"{domain}_copy.html" if domain else "website_copy.html"

def save_website_html(url):
    try:

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url


        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        filename = get_valid_filename(url)
        counter = 1
        while os.path.exists(filename):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{counter}{ext}"
            counter += 1

        soup = BeautifulSoup(response.text, 'html.parser')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        print(f"\nSuccess! HTML saved as: {filename}")
        print(f"Full path: {os.path.abspath(filename)}")

    except requests.exceptions.RequestException as e:
        print(f"\nError downloading the website: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def main():
    print("=== Website HTML Copier ===")
    print("Copies a website's HTML and saves it with the domain name")
    
    while True:
        url = input("\nEnter website URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ('exit', 'quit', 'q'):
            break
            
        if not url:
            print("Please enter a valid URL")
            continue
            
        save_website_html(url)
        
        choice = input("\nCopy another website? (y/n): ").lower()
        if choice not in ('y', 'yes'):
            break

    print("\nProgram closed. Press Enter to exit...")
    input()     # discord : emir.net :3

if __name__ == "__main__":
    main()
