# coding:utf-8
"""
author:周栋梁
time:2017/6/10
"""
import numpy as np
import pandas as pd
import seaborn; seaborn.set()
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def convert(num, circle):
    """
    返回对应刻度的时间格式为h:mm或者hh:mm
    :param num: x轴刻度
    :param circle: 周期
    :return: 对应刻度的时间格式为h:mm或者hh:mm
    """
    return str(int((num * circle) // 60 % 24)) + ":" + str(int((num * circle) % 60)).zfill(2)
def process(circle):
    """
    处理原始数据，生成中间结果数据，以及绘制改进的K线
    :param circle: 设定对应的时间周期，单位为分钟
    :return: null
    """
    path = './original_data/SH600829.csv'
    origin_data = pd.read_csv(path)
    origin_data = origin_data[origin_data['time'] >= 93000]
    origin_data['time'] = origin_data['time'] % 100 + (origin_data['time'] // 100 % 100) * 60 + (origin_data['time'] // 10000) * 60 * 60
    origin_data['time'] = origin_data['time'] // (60 * circle)
    time = origin_data['time']
    time_lst = np.array(time)
    time_lst = np.unique(time_lst)
    lst = []
    for time_key in time_lst:
        tmp_data = origin_data[origin_data['time'] == time_key]
        begin_index = tmp_data.index.min()
        end_index = tmp_data.index.max()
        open = tmp_data.loc[[begin_index]]['price'][begin_index]
        close = tmp_data.loc[[end_index]]['price'][end_index]
        high = tmp_data['price'].max()
        low = tmp_data['price'].min()
        price_lst = tmp_data['price']
        price_lst = np.unique(price_lst)
        max_amount = 0
        max_amount_price = 0

        for price_key in price_lst:
            tmp2_data = tmp_data[tmp_data['price'] == price_key]
            cum_amount = tmp2_data['amount'].sum()
            if cum_amount > max_amount:
                max_amount = cum_amount
                max_amount_price = price_key
        lst.append(list([time_key,open,high,low,close,max_amount_price]))
    intermidate_data = pd.DataFrame(data=lst,columns=['time', 'open', 'high', 'low', 'close','max_amount_price'])
    intermidate_data.to_csv('./intermidate_data/周期为'+str(circle) +'分钟蜡烛图中间处理数据.csv',index=False)
    fig, ax = plt.subplots()
    candlestick_ohlc(ax,lst, width=0.1, colorup='r', colordown='g', alpha=1.0)
    fs = circle * 2
    if fs >= 25:
        fs = 25
    plt.yticks(fontsize=25)
    plt.xticks(fontsize=fs)
    plt.title(u"股票代码：SH600829 蜡烛图",fontsize=25)
    plt.xlabel(u"时间",fontsize=25)
    plt.ylabel(u"股价（元）",fontsize=25)
    x_ticks = time_lst
    x_labels = [convert(item,circle) for item in time_lst]
    plt.setp(ax, xticks=x_ticks - 0.5, xticklabels=x_labels)
    for time_amount in time_lst:
        plt.plot([time_amount - 0.2, time_amount + 0.2],[intermidate_data.loc[intermidate_data[intermidate_data['time'] == time_amount].index.min()]['max_amount_price'],intermidate_data.loc[intermidate_data[intermidate_data['time'] == time_amount].index.min()]['max_amount_price']], 'b-')
    plt.tight_layout(True)
    plt.grid(True)
    fig.set_size_inches(35, 23)
    plt.savefig(u'./results/周期为' + str(circle) + '分钟的蜡烛图',dpi=300,bbox_inches='tight')


if __name__ == '__main__':
    time_circle = [1,3,5,10,15,30]
    for circle in time_circle:
        process(circle)
        print(u'周期为' + str(circle) + u'分钟数据处理完毕')