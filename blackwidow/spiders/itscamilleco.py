from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from blackwidow.items import HeelsItem


class CamilleTriesToBlogSpider(CrawlSpider):

    name = 'itscamilleco'
    allowed_domains = ['itscamilleco.com', ]
    start_urls = [
        'http://itscamilleco.com/',
    ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'page/\d+/', ),  # http://itscamilleco.com/page/2/
                restrict_xpaths=('//div[contains(@class, "pagination")]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+/', ),  # http://itscamilleco.com/2013/11/beach-baby/
                restrict_xpaths=('//*[@id="main"]', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = HeelsItem()

        item['comment'] = hxs.select('//title/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="main"]//div[contains(@class, "post")]//div[contains(@class, "entry")]//img/@src').extract()
        item['source_url'] = response.url

        return item
