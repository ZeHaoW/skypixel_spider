import scrapy
from scrapy import Request
from skypixel_spider.items import SkypixelPhotosItem

class SkypixelSpider(scrapy.Spider):
    name = "skypixel_photos_task"
    count = 1
    start_urls = ["https://www.skypixel.com/api/website/resources/photos?page=%s&page_size=12"]
    ITEM_PIPELINES = {'skypixel_spider.pipelines.SkypixelPhotosPipeline': 1}
    IMAGES_STORE = '/skypixel_spider/spiders/photos'
    IMAGE_EXPIRES = 90

    def parse(self, response):
        item = SkypixelPhotosItem()
        item['imageurls'] = []
        jsonObj = json.loads(response.body_as_unicode())
        jars = jsonObj['items']
        for n in jars:
            photo_url = n['image'] + '@!1200'
            item['imageurls'].append(photo_url)
        count += 1
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)

    def start_requests(self):
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)
