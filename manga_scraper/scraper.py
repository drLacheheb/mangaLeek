from playwright.async_api import async_playwright
from config import VIEWPORT_SIZE,ZOOM_LEVEL

async def launch_browser():
    """launch the browser with a very low zoom"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT_SIZE,
        )
        page = await context.new_page()

        # set zoom level to low
        await page.add_style_tag(content=f"body {{ zoom: {ZOOM_LEVEL}; }}")
        
        return page, browser

async def scrape_manga_page(page, url):
    async def scrape_manga_details(manga):
        """scrape the details of a single manga item"""
        # image URL
        img_elem = await manga.query_selector(".item-thumb img")
        img_url = await img_elem.get_attribute("src") if img_elem else None
        
        # manga title
        title_elem = await manga.query_selector(".post-title a")
        title = await title_elem.inner_text() if title_elem else None
        
        # rating
        rating_elem = await manga.query_selector(".post-total-rating .score")
        rating = await rating_elem.inner_text() if rating_elem else None
        
        # last chapter and date
        chapter_elem = await manga.query_selector(".list-chapter .chapter-item a")
        chapter_url = await chapter_elem.get_attribute("href") if chapter_elem else None
        chapter_text = await chapter_elem.inner_text() if chapter_elem else None
        date_elem = await manga.query_selector(".list-chapter .chapter-item .post-on")
        date = await date_elem.inner_text() if date_elem else None

        return {
            "Title": title,
            "Image URL": img_url,
            "Rating": rating,
            "Last Chapter": chapter_text,
            "Chapter URL": chapter_url,
            "Date of Last Chapter": date
        }

    manga_data = []
    await page.goto(url)
    await page.wait_for_selector("#loop-content")

    # manga item
    manga_list = await page.query_selector_all(".page-listing-item")
    for manga in manga_list:
        manga_details = await scrape_manga_details(manga)
        manga_data.append(manga_details)

    return manga_data