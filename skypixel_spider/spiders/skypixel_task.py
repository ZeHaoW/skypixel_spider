import scrapy
import json
from scrapy import Request
from skypixel_spider.items import SkypixelPhotosItem

class SkypixelSpider(scrapy.Spider):
    name = "skypixel_photos_task"
    count = 1
    start_urls = ["https://www.skypixel.com/api/website/resources/photos?page=%s&page_size=12"]
    # ITEM_PIPELINES = {'skypixel_spider.pipelines.SkypixelPhotosPipeline': 1}
    # IMAGE_EXPIRES = 90

    def parse(self, response):
        item = SkypixelPhotosItem()
        item['image_urls'] = []
        jsonObj = json.loads(response.body_as_unicode())
        jars = jsonObj['items']
        for n in jars:
            photo_url = n['image'] + '@!1200'
            item['image_urls'].append(photo_url)
        self.count++
        yield item
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)

    def start_requests(self):
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)
