from utils import *

import pandas as pd

def load_daily_data(start_date, end_date):
    trade_dates = get_trade_day(start_date, end_date)  # 获取交易日列表
    stock_dict = {}  # 存储所有股票数据
    valid_stocks = set()  # 记录第一天的股票池
    first_day = True  # 标记是否为第一天

    for date in trade_dates:
        df = pro.daily(trade_date=date)  # 获取当天数据
        filtered_df = df[df["ts_code"].str.startswith(("000", "600"))]  # 筛选000/600开头的股票

        if first_day:
            # 记录第一天的所有股票代码，并存入 stock_dict
            valid_stocks = set(filtered_df["ts_code"])  # 记录基准股票池
            for ts_code, stock_data in filtered_df.groupby("ts_code"):
                stock_dict[ts_code] = {"data":stock_data}
            first_day = False
        else:
            # 仅保留第一天出现过的股票
            filtered_df = filtered_df[filtered_df["ts_code"].isin(valid_stocks)]
            updated_stocks = set()

            # 更新已有股票数据
            for ts_code, stock_data in filtered_df.groupby("ts_code"):
                stock_dict[ts_code]['data'] = pd.concat([stock_dict[ts_code]['data'], stock_data])
                updated_stocks.add(ts_code)

            # 对于未更新的股票（停牌），用前一天数据填充
            missing_stocks = valid_stocks - updated_stocks
            for ts_code in missing_stocks:
                last_data = stock_dict[ts_code]['data'].iloc[-1].copy()  # 复制前一天数据
                last_data["trade_date"] = date  # 修改日期
                stock_dict[ts_code]['data'] = pd.concat([stock_dict[ts_code]['data'], last_data.to_frame().T])  # 补全数据
    return stock_dict   

def load_information(stock_dict):
    
    information_dict = {}
    for ts_code in tqdm(stock_dict.keys()):
        code = ts_code.split(".")[0]
        info = get_infomation(code)
        information_dict[ts_code] = {
            'name': info.get("股票简称", ""),
            'industry': info.get("行业", ""),
            'totals': info.get("总股本", "")
        }
    return information_dict

def save_to_json(start_date,end_date, filename="stock_data.json",information_file = "information.json"):
    stock_dict = load_daily_data(start_date, end_date)
    infomation_dict = load_information(stock_dict)
    print(infomation_dict)
    # 转换 stock_dict 为可以写入 JSON 的格式
    data_to_write = {}
    for ts_code, stock_data in stock_dict.items():
        # 转换 DataFrame 为字典列表
        print(infomation_dict[ts_code])
        stock_data_list = stock_data['data'].to_dict(orient='records')
        data_to_write[ts_code] = {
            "name": infomation_dict[ts_code]["name"],
            "industry": infomation_dict[ts_code]["industry"],
            "totals": infomation_dict[ts_code]["totals"],
            "data": stock_data_list  # 添加股票的所有交易数据
        }

    # 写入 JSON 文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_to_write, f, ensure_ascii=False, indent=4)  # 使用 indent 格式化输出
    with open(information_file, 'w', encoding='utf-8') as f:
        json.dump(infomation_dict, f, ensure_ascii=False, indent=4)  # 使用 indent 格式化输出
if __name__ == '__main__':
    save_to_json("20220101", "20250226", "full_data/stock_data.json", "full_data/information.json")