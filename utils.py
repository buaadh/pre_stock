import tushare as ts
import pandas as pd
import akshare as ak
import json
from tqdm import tqdm
#设置你的token，登录tushare在个人用户中心里拷贝
ts.set_token('2daab08260e324ea51079798da46c9a53e54a2b16cbf6bae59a930c8')
pro = ts.pro_api()

def get_trade_day(start_date, end_date,time_out=10):
    try:
        df = pro.daily(ts_code='000001.SZ', start_date=start_date, end_date=end_date)
    except Exception as e:
        time_out -= 0
        if time_out < 0:
            raise TimeoutError('time out')
    trade_date = df['trade_date'].tolist()
    trade_date.reverse()
    return trade_date

def get_realtime_data(ts_code,time_out = 10):
    try:
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    except Exception as e:
        time_out -= 0
        if time_out < 0:
            raise TimeoutError('time out')
    return stock_zh_a_spot_em_df[stock_zh_a_spot_em_df['代码'] == ts_code]

def get_infomation(ts_code,time_out = 10):
    try:
        stock_individual_info_em_df = ak.stock_individual_info_em(symbol=ts_code)
    except Exception as e:
        time_out -= 0
        if time_out < 0:
            raise TimeoutError('time out')
    # 将 DataFrame 转换为字典
    result_dict = dict(zip(stock_individual_info_em_df['item'], stock_individual_info_em_df['value']))
    return result_dict

def get_hot_rate(ts_code):
    code = "".join(ts_code.split('.').reverse())
    stock_hot_rank_latest_em_df = ak.stock_hot_rank_latest_em(symbol=code)
    result_dict = dict(zip(stock_hot_rank_latest_em_df['item'], stock_hot_rank_latest_em_df['value']))
    return result_dict
if __name__ == '__main__':
    print(get_infomation())