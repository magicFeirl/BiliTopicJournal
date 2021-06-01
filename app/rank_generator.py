def generate(raw_data):
    """计算加权总分
    Args:
        raw_data: 原始数据

    Returns:
        一个元组，分别是:
            * 总排行列表，内含 {视频 av 号、标题、总分} 字典
            * 原创排行列表，数据同上"""
    import math

    ori = []
    non_ori = []

    # 遍历每项数据
    for item in raw_data:
        # 获取要加权的元素
        view = item['view']
        stat = item['stat']
        favorite = stat['favorite']
        like = stat['like']
        danmaku = stat['danmaku']
        coin = stat['coin']
        share = stat['share']
        # reply = stat['reply']

        score = view + like * 10 + (danmaku + coin) * 20 + favorite * 30 + share * 50

        """
        if view == 0:
            view = 1


        exp_P = 1 # 分P计分不适用于月刊统计（有些视频P数很多但其他数据很少，结果总分反而非常高）
        exp_A = (200000 + view) / (2 * view)
        exp_B = ((favorite * 20) + (coin * 10)) / (view + coin * 10 + reply * 50)

        score = view * exp_P * exp_A + reply * exp_B * 50 + coin * exp_B + favorite * 20
        """


        result = {
            'aid': 'av' + str(item['aid']),
            'title': item['title'],
            'score': score # math.ceil(score)
        }

        # 如果是原创，添加到原创榜
        if item['original']:
            ori.append(result)
        else: # 否则将结果添加到搬运榜
            non_ori.append(result)

    non_ori.sort(key=lambda x: x['score'], reverse=True)
    ori.sort(key=lambda x: x['score'], reverse=True)

    return format_data(ori), format_data(non_ori)


def format_data(rank_list):
    result = []

    for idx, item in enumerate(rank_list):
        result.append(' '.join([str(idx), str(item['aid']), item['title'], str(item['score'])]))

    return '\n'.join(result)


