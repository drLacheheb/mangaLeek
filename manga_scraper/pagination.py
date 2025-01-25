async def get_next_page_url(page):
    """get the URL of the next page from the pagination controls"""
    next_button = await page.query_selector(".nextpostslink")
    if next_button:
        next_page_url = await next_button.get_attribute("href")
        return next_page_url
    return None