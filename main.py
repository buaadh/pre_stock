from get_daily_data import *
from get_extend_info import *
from get_market_feature import *

START_DATE = "20220101"
END_DATE = "20220106"

if __name__ == '__main__':
    stocks = get_stock_history(START_DATE, END_DATE,output_file='full_data/trade_data.json')
    base_info = load_base_information(stocks)
    bk_info = load_stock_bk(stocks)
    merged_dict = {}
    for key in base_info:
        merged_dict[key] = base_info[key]
        merged_dict[key]["bk"] = bk_info[key]
    with open('full_data/base_data.json', 'w', encoding='utf-8') as f:
        json.dump(merged_dict, f, ensure_ascii=False, indent=4)
    market_index = get_market_index(START_DATE, END_DATE)
    with open('full_data/market_index.json', 'w', encoding='utf-8') as f:
        json.dump(market_index, f, ensure_ascii=False, indent=4)
    print("Done!")

