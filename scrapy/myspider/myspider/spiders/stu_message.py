import scrapy


class StuMessageSpider(scrapy.Spider):
    name = "stu_message"
    allowed_domains = ["zy.upln.cn"]
    start_urls = [
        "https://zy.upln.cn/index.html",
    ]

    def parse(self, response):
        """
        爬虫程序入口
        :param response:
        :return:
        """

        # 获取主页链接中所有的跳转链接并依次跳转
        for href in response.css("table.ui-table.ui-table-noborder tbody a::attr(href)").getall():
            # 创建新的请求跳转链接并执行回调函数对新链接进行内容的爬取
            yield response.follow(href, callback=self.parse_href)

    def parse_href(self, response):
        """
        进入到具体大学专业网址在进行一次跳转
        :param response:
        :return:
        """
        for href in response.css('td:contains("点击查看详情") a::attr(href)').getall():
            # 进入专业详情界面
            yield response.follow(href, callback=self.get_data)

    def get_data(self, response):
        """
        爬取具体的专业内容
        :param response:
        :return:
        """
        # 使用CSS选择器提取数据
        fields = {
            "高校名称及代码": 'tr:contains("高校名称及代码") td:nth-child(2)::text',
            "专业名称及代码": 'tr:contains("专业名称及代码") td:nth-child(2)::text',
            "专业英文名称": 'tr:contains("专业英文名称") td:nth-child(4)::text',
            "学制": 'tr:contains("学制") td:nth-child(2)::text',
            "修业年限": 'tr:contains("修业年限") td:nth-child(4)::text',
            "学位授予门类": 'tr:contains("学位授予门类") td:nth-child(2)::text',
            "专业设置时间": 'tr:contains("专业设置时间") td:nth-child(2)::text',
            "招生方式": 'tr:contains("招生方式") td:nth-child(2)::text',
            "专业教师数": 'tr:contains("专业教师数") td:nth-child(2)::text',
            "本科学生数": 'tr:contains("本科学生数") td:nth-child(2)::text',
            "招生类型": 'tr:contains("招生类型") td:nth-child(4)::text',
            "外聘教师数": 'tr:contains("外聘教师数") td:nth-child(4)::text',
            "首次招生时间": 'tr:contains("首次招生时间") td:nth-child(4)::text',
            "主干学科": 'tr:contains("主干学科") td:nth-child(2)::text',
            "专业主干课程及简介": 'tr:contains("专业主干课程及简介") td:nth-child(2)::text',
            "专业简介": 'tr:contains("专业简介") td:nth-child(2) p.duan::text',
            "高层次人才情况": 'tr:contains("高层次人才情况") td:nth-child(2) ul.ui-list',
            "本科教学工程情况": 'tr:contains("本科教学工程情况") td:nth-child(2) ul.ui-list',
        }

        data = {}
        for field, selector in fields.items():
            if field == "高层次人才情况":
                # 组合返回
                people_final_res = self.dispose_special_fields(response, "高层次人才情况")
                data[field] = ' '.join(people_final_res)
            elif field == '本科教学工程情况':
                # 组合返回
                teach_final_res = self.dispose_special_fields(response, "本科教学工程情况")
                data[field] = ' '.join(teach_final_res)
            elif field == "专业简介":
                # 对数据进行去除空格的处理
                texts = [text.strip() for text in response.css(selector).getall()]
                data[field] = ''.join(texts)
            else:
                data[field] = response.css(selector).get()

        yield data

    def dispose_special_fields(self, response, field):
        """
        对高层次人才情况与本科教学工程情况进行特殊处理
        :param response:
        :return:
        """

        re_name_text = f'tr:contains({field}) td:nth-child(2) ul.ui-list span.datahl::text'
        # 获取高层次人才情况中的种类
        name_list = response.css(re_name_text).getall()
        re_peoples_text = f'tr:contains({field}) td:nth-child(2) ul.ui-list li::text'
        # 获取高层次人才情况中的人数
        people_list = response.css(re_peoples_text).getall()
        # 组合返回
        final_res = list(map(lambda x: x[0] + x[1], zip(name_list, people_list)))

        return final_res
