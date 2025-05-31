# data-extractor.py

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self, filename):
        os.makedirs(self.save_at, exist_ok=True)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        os.makedirs(self.save_at, exist_ok=True)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    coordinates = url.split('/@')[-1].split('/')[0]
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int, default=100)
    args = parser.parse_args()

    search_list = [args.search] if args.search else []

    if not search_list:
        input_file_path = os.path.join(os.getcwd(), 'input.txt')
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                search_list = [line.strip() for line in file if line.strip()]
        if not search_list:
            print('Error: No search terms provided.')
            sys.exit()

    total = args.total

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)

        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index} - {search_for}".strip())

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)
                current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()

                if current_count >= total:
                    break
                if current_count == previously_counted:
                    break
                previously_counted = current_count

            listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
            listings = [listing.locator("xpath=..") for listing in listings]
            print(f"Scraped {len(listings)} listings")

            business_list = BusinessList()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)

                    business = Business()
                    name_attr = listing.get_attribute('aria-label') or ""
                    business.name = name_attr.strip()

                    address = page.locator('//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]')
                    business.address = address.inner_text().strip() if address.count() > 0 else ""

                    website = page.locator('//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]')
                    business.website = website.inner_text().strip() if website.count() > 0 else ""

                    phone = page.locator('//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]')
                    business.phone_number = phone.inner_text().strip() if phone.count() > 0 else ""

                    review_count = page.locator('//button[@jsaction="pane.reviewChart.moreReviews"]//span')
                    business.reviews_count = int(review_count.inner_text().split()[0].replace(',', '')) if review_count.count() > 0 else None

                    review_avg = page.locator('//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]')
                    review_str = review_avg.get_attribute('aria-label') if review_avg.count() > 0 else ""
                    if review_str:
                        business.reviews_average = float(review_str.split()[0].replace(',', '.'))

                    business.latitude, business.longitude = extract_coordinates_from_url(page.url)
                    business_list.business_list.append(business)
                except Exception as e:
                    print(f"Error: {e}")

            filename = f"google_maps_data_{search_for}".replace(' ', '_')
            business_list.save_to_excel(filename)
            business_list.save_to_csv(filename)

        browser.close()

if __name__ == "__main__":
    main()
