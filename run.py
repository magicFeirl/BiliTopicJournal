"""计算 tag 排名并输出"""
import os
import json
from datetime import datetime

from app import rank_generator
from app.date_filter import DateFilter
from app.tag_info_crawler import TagInfoCrawler

def main():
    tags = [1826, 6708, 2494330, 2526823]

    df = DateFilter()
    crawler = TagInfoCrawler()

    r = crawler.fetch_many(tags, 1, 10, date_filter=df.yesterday)

    # 原创 & 搬运 结果文本
    ori, non_ori = rank_generator.generate(r)

    content = ''

    if ori:
        content = '原创:\n\n' + ori + '\n\n\n\n'

    if non_ori:
        content += '搬运:\n\n' + non_ori


    print('*' * 30)
    print(rs)

if __name__ == '__main__':
    main()
