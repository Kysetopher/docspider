import scrapy

class DocSpider(scrapy.Spider):
    name = 'doc_spider'
    start_urls = ['https://docs.pinecone.io/reference/api/introduction']

    async def parse(self, response):
        # Use Playwright to handle JavaScript-rendered pages
        page = response.meta['playwright_page']
        await page.click('selector-for-tab')  # Update this selector to click on tabbed interfaces
        content = await page.content()
        clean_text = scrapy.utils.markup.remove_tags(content)  # Clean HTML tags
        yield {'text': clean_text}
        # Follow other URLs within the same domain
        links = await page.query_selector_all('a')
        for link in links:
            href = await page.evaluate('(element) => element.href', link)
            if 'docs.pinecone.io' in href:
                yield response.follow(href, self.parse)