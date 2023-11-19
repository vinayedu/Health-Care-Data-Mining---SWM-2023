import scrapy

class PatientInfoSpider(scrapy.Spider):

    name = "patient_info"

    def start_requests(self):
        url_prefix = 'https://patient.info/forums/index-'
        alphabet = 'A'
        i = 0

        while i < 26:
            url = f'{url_prefix}{chr(ord(alphabet) + i)}'
            yield scrapy.Request(url=url, callback=self.parse)
            i += 1

    def parse(self, response):
        a_to_z_groups = response.xpath("//div[@class='disc-forums disc-a-z']")
        symptom_rows_links = a_to_z_groups.xpath(".//tr[@class='row-0']//a/@href")[:]

        for symptom_link in symptom_rows_links:
            symptom_complete_link = response.urljoin(symptom_link.get())
            yield scrapy.Request(url=symptom_complete_link, callback=self.parse_posts_list)

    def parse_posts_list(self, response):
        disease = response.xpath("//h1[@class='articleHeader__title masthead__title']/text()").get().strip()
        posts = response.xpath("//li[@class='disc-smr cardb']")[:]

        for post_heading in posts:
            post_link_anchor_tag = post_heading.xpath(".//h3[@class='post__title']//a/@href")
            post_link = response.urljoin(post_link_anchor_tag.get())
            my_dict = {
                'contentType': 'disease',
                'disease': disease,
                'postLink': post_link
            }
            yield my_dict
            yield scrapy.Request(url=post_link, callback=self.parse_post)

    def parse_post(self, response):
        post_link = response.url
        post_heading = response.xpath("//h1[@class='u-h1 post__title']/text()").get()
        post_content_paras = response.xpath("//div[@class='post__content']/p/text()")
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
