from utils import *

import pandas as pd

def get_stock_history(start_date: str, end_date: str, adjust: str = "", output_file: str = "stock_data.json",time_out = 10):
    """
    获取所有以600和100开头的A股股票的历史行情数据，并存储为JSON文件。
    
    :param start_date: 查询开始日期，格式 'YYYYMMDD'
    :param end_date: 查询结束日期，格式 'YYYYMMDD'
    :param adjust: 复权类型，'qfq' 表示前复权，'hfq' 表示后复权，默认 'qfq'
    :param output_file: 输出的JSON文件名，默认 'stock_data.json'
    """
    # 获取所有 A 股股票列表
    stock_list_df = ak.stock_zh_a_spot_em()
    
    # 过滤以600和100开头的股票代码
    stock_codes = stock_list_df["代码"].astype(str)
    filtered_stocks = stock_codes[stock_codes.str.startswith(("000000", "60000"))]
    
    stock_data = {}
    
    for symbol in tqdm(filtered_stocks):
        TIME_LIMIT = time_out
        while True:
            try:
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust=adjust)
                if df.empty:
                    raise ValueError(f"获取 {symbol} 数据为空")
                df["日期"] = df["日期"].astype(str)
                stock_data[symbol] = df.to_dict(orient="records")
                break
            except Exception as e:
                time.sleep(1)
                print(f"获取 {symbol} 数据时出错: {e}")
                TIME_LIMIT -= 1
                if TIME_LIMIT < 0:
                    break
    
    # 将数据写入 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=4)
    
    print(f"数据已保存至 {output_file}")
    return stock_codes


if __name__ == '__main__':
    get_stock_history(start_date="20220101", end_date="20220106")