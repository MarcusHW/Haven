import scrapy

from Aoisolas.Aoisolas.items import AoisolasItem


class AiosolaspiderSpider(scrapy.Spider):
    name = "AoiSola"
    allowed_domain = ["www.mm131.com"]
    start_urls = ['http://www.mm131.com/xinggan/',
                  'http://www.mm131.com/qingchun/',
                  'http://www.mm131.com/xiaohua/',
                  'http://www.mm131.com/chemo/',
                  'http://www.mm131.com/qipao/',
                  'http://www.mm131.com/mingxing/']

    def parse(self, response):
        list = response.css(".list-left dd:not(.page)")
        imgurl = img.css("a::attr(href)").extract_first()
        imgurl2 = str(imgurl)
        print(imgurl2)
        next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_First()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
        yield scrapy.Request(imgurl2, callback=self.content)

    def content(self, response):
        item = AoisolasItem()
        item['name'] = response.css(".content h5::text").extract_first()
        item['imgUrl'] = response.css(".content-pic img::attr(src)").extract_first()
        yield item
        next_url = response.css(".page-ch:last-child::attr(href)").extract_first()

        if next_url is not None:
            yield response.follow(next_url, callback=self.content)
