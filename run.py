"""计算 tag 排名并输出到本地"""
import os
import json
from datetime import datetime

from app import rank_generator
from app.date_filter import DateFilter
from app.tag_info_crawler import TagInfoCrawler

def save_to_file(filename: str, raw_data: list, ori: str, non_ori: str):
    dirpath = f'./data/{filename}'
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    fullpath = os.path.join(os.getcwd(), dirpath, filename)

    with open(f'{fullpath}_raw_data.json', 'w', encoding='utf-8') as f:
        def datetime2str(obj):
            if isinstance(obj, datetime):
                return str(obj)
            return obj

        json.dump(raw_data, f, ensure_ascii=False, default=datetime2str)

    with open(f'{fullpath}_original.txt', 'w', encoding='utf-8') as f:
        content = '原创榜'.center(45, '*') + '\n' + ori
        f.write(content)

    with open(f'{fullpath}_non_original.txt', 'w', encoding='utf-8') as f:
        content = '搬运榜'.center(45, '*') + '\n' + non_ori
        f.write(content)


def main():
    # 要生成月刊的 tag id 列表
    tags = [1826, 6708, 2494330, 2526823]

    df = DateFilter()
    crawler = TagInfoCrawler()

    # 获取指定 tags 的昨日视频更新信息
    # r = crawler.fetch_many(tags, 1, 10, date_filter=df.yesterday)

    now = datetime.now()
    year, month = now.year, now.month

    # 如果是今年一月份，上个月是去年的 12 月
    if month == 1:
        year = year - 1
        month = 12
    else: # 否则上个月就是这个月 -1
        month = month - 1

    # 获取指定 tags 的上个月的视频更新信息
    r = crawler.fetch_many(tags, 1, 1, date_filter=df.month, args=(year, month))

    # 原创 & 搬运 结果文本
    ori, non_ori = rank_generator.generate(r)

    # 结果输出到 ./data/{year}_{month}/ 下
    save_to_file(f'{year}_{month}', r, ori, non_ori)


if __name__ == '__main__':
    main()
