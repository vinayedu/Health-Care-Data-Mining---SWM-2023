import scrapy

class PatientInfoSpider(scrapy.Spider):
    name = "drugs"

    def start_requests(self):
        url = 'https://www.drugs.com/answers/conditions/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        condition_groups = response.xpath("//ul[@class='column-span column-span-3']/li/a/@href")
        print("#########   1  #############")
        print("############################")
        print(condition_groups)

        for condition in condition_groups:
            condition_link = response.urljoin(condition.get()) + "questions/"
            print(condition_link)
            yield scrapy.Request(url=condition_link, callback=self.parse_support_group)

        print("############################")
        print("############################")

    def parse_support_group(self, response):
        print("#########   2  #############")
        print("############################")
        disease = response.xpath("//div[@class='groupHead']/h1/text()").get()
        disease = disease.replace("Questions", "").strip()
        posts = response.xpath("//div[@class='questionList visited']/div[@class='listContent']/h2/a/@href")
        print("Count:", len(posts))
        print("disease:"+disease+":")

        for post_heading in posts:
            post_link = response.urljoin(post_heading.get())
            print(post_link)
            my_dict = {
                'contentType': 'disease',
                'disease': disease,
                'postLink': post_link
            }
            yield my_dict
            yield scrapy.Request(url=post_link, callback=self.parse_post)

        next_link = response.xpath("//li[@class='ddc-paging-item-next ddc-paging-item-span2']/a/@href")
        print("next_link:", next_link)

        if len(next_link) > 0:
            next_complete_link = response.urljoin(next_link.get())
            yield scrapy.Request(url=next_complete_link, callback=self.parse_support_group)
            print("next_complete_link:", next_complete_link)

        print("############################")
        print("############################")

    def parse_post(self, response):
        print("#########   3  #############")
        print("############################")
        post_link = response.url
        content_div = response.xpath("//div[@class='postWrap clearAfter showInvisible']")
        post_heading = content_div.xpath(".//h1/text()").get()
        post_content_paras = content_div.xpath(".//div[@class='postContent']/p/text()")
        post_content = ''

        for para in post_content_paras:
            post_content += para.get() + ' '

        item = {
            'contentType': 'userPost',
            'postLink': post_link,
            'postHeading': post_heading,
            'postContent': post_content
        }

        yield item
        print(item)
        print("############################")
        print("############################")
