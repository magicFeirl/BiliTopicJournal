import time
import datetime
import traceback

import requests
import pytz

class TagInfoCrawler():
    def __init__(self):
        self.cntz = pytz.timezone('Asia/Shanghai')
        self.aid_set = set()

    def request(self, method, url, data=None, params=None, headers=None):
        """发请求"""
        if headers is None:
            headers = {
                'user-agent': 'wasp',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }

        return requests.request(method, url, data=data, params=params, headers=headers)

    def _fetch_one(self, tid, pn, ps=20):
        api = 'https://api.bilibili.com/x/tag/detail'

        params = {
            'pn': pn,
            'ps': ps,
            'tag_id': tid
        }

        rj = self.request('GET', api, params=params).json()

        if not rj['data']['news']['archives']:
            return None

        return self._get_archives(rj)

    def fetch_many(self, tids, begin, end, date_filter=None, args=(), ps=20):
        result = []

        if not isinstance(tids, list):
            tids = [tids]

        for tid in tids:
            has_next = True
            print('开始获取 tag: {} 的数据'.format(tid))

            try:
                for pn in range(begin, end + 1):
                    if not has_next:
                        break

                    # 抓取 json
                    rj = self._fetch_one(tid, pn, ps)

                    if rj is None:
                        print('tag: {} 第 {} 页无数据'.format(tid, pn))
                        break
                    else:
                        print('第 {} 页数据已获取'.format(pn))

                    if date_filter is None:
                        result.extend(rj)
                    else:
                        for archive in rj:
                            # 数据是否在指定日期内 数据是否已经比指定日期的最小日期还要小
                            in_range, lt_left = date_filter(archive['pubdate'], *args)

                            # 如果比最小日期还要小，由于是按时间排序的，所以后面的数据不可能在时间范围内了，直接 break
                            if lt_left:
                                print('当前数据时间已小于最小时间')
                                has_next = False
                                break

                            if in_range:
                                result.append(archive)

                    if pn != end:
                        print('休眠 0.5s')
                        time.sleep(0.5)
            except:
                traceback.print_exc()

            print()

        return result

    def _get_archives(self, json_data):
        result = []

        archives = json_data['data']['news']['archives']

        for archive in archives:
            aid = str(archive['aid'])
            stat = archive['stat']
            title = archive['title'].strip()
            view =  stat['view']
            original = (archive['copyright'] == 1)
            desc = ''
            videos = archive['videos']

            if 'desc' in archive:
                desc = archive['desc']

            pubdate = datetime.datetime.fromtimestamp(archive['pubdate'], tz=self.cntz)
            pubdate = pubdate.replace(tzinfo=None)

            if not aid in self.aid_set:
                result.append({
                    'aid': aid,
                    'stat': stat,
                    'title': title,
                    'view': view,
                    'original': original,
                    'desc': desc,
                    'pubdate': pubdate,
                    'videos': videos
                })

                self.aid_set.add(aid)

        return result
