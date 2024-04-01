import os
from scrapy.cmdline import execute

# 获取项目文件夹的路径
project_dir = os.path.dirname(os.path.abspath(__file__))

# 将项目文件夹设置为当前工作目录
os.chdir(project_dir)

# 执行Scrapy命令
execute(['scrapy', 'crawl', 'stu_message'])