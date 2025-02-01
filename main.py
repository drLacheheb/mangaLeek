import asyncio

from manga_scraper.scraper import launch_browser, scrape_manga_page
from manga_scraper.pagination import get_next_page_url
from manga_scraper.data_handler import save_to_csv
from manga_scraper.config import BASE_URL

async def main():
    """scrape data with pagination and save it"""
    page, browser, playwright = await launch_browser()
    
    current_page_url = BASE_URL
    all_manga_data = []

    while current_page_url:
        print(f"scraping page: {current_page_url}")
        manga_data = await scrape_manga_page(page, current_page_url)
        all_manga_data.extend(manga_data)

        # get the next page
        current_page_url = await get_next_page_url(page)

        # if there is no next page
        if not current_page_url:
            print("No more pages to scrape.")
            break

    # save the scraped data to CSV
    save_to_csv(all_manga_data)

    await browser.close()
    await playwright.stop()


asyncio.run(main())
