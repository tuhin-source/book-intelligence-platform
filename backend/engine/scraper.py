import os
import django
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- MANDATORY DJANGO SETUP ---
# This allows the script to access your Book model and MySQL database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Book

def run_book_scraper():
    print("🚀 Starting Selenium Scraper...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Runs in the background
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # We are scraping a demo site designed for practice
    driver.get("https://books.toscrape.com/catalogue/category/books/science_22/index.html")
    time.sleep(2)

    # Find the book elements
    items = driver.find_elements(By.CSS_SELECTOR, ".product_pod")

    for item in items[:10]: # Grab the first 10 books
        title = item.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
        url = item.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("href")
        price = item.find_element(By.CLASS_NAME, "price_color").text
        
        # Save to MySQL via Django ORM
        book, created = Book.objects.get_or_create(
            title=title,
            defaults={
                'book_url': url,
                'rating': price,
                'author': "Science Author",
                'description': f"A fascinating science book found for {price}."
            }
        )
        
        if created:
            print(f"✅ Saved: {title}")
        else:
            print(f"⏭️  Already exists: {title}")

    driver.quit()
    print("✨ Scraping and Database population complete!")

if __name__ == "__main__":
    run_book_scraper()