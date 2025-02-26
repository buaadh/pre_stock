from utils import *

def load_base_information(stocks):
    information_dict = {}
    for code in tqdm(stocks, desc="Loading information"):

        info = get_infomation(code)
        information_dict[code] = {
            'name': info.get("股票简称", ""),
            'industry': info.get("行业", ""),
            'totals': info.get("总股本", "")
        }
    return information_dict


# 获取某个板块下所有股票
def get_stocks_in_concept(concept_name,time_out = 10):
    while True:
        try:
            stock_board_concept_cons_em_df = ak.stock_board_concept_cons_em(symbol=concept_name)
            break
        except Exception as e:
            time.sleep(1)
            time_out -= 1
            if time_out < 0:
                raise TimeoutError('time out')
    return stock_board_concept_cons_em_df['代码']

# 处理所有股票，返回字典
def load_stock_bk(stocks):
    all_concepts = get_all_concept_names()  # 获取所有概念板块
    stock_concepts = {stock: [] for stock in stocks}  # 为每支股票创建一个空的概念列表

    # 遍历所有概念板块
    for concept in tqdm(all_concepts):
        concept_stocks_df = get_stocks_in_concept(concept)
        concept_stocks_set = set(concept_stocks_df.tolist())  # 当前板块下的所有股票代码

        # 遍历输入的股票，检查是否在当前板块中
        for stock_code in stock_concepts.keys():
            if stock_code in concept_stocks_set:
                stock_concepts[stock_code].append(concept)  # 更新该股票的概念板块列表
    return stock_concepts


stocks = ['600000','600004']
base_info = load_base_information(stocks)
bk_info = load_stock_bk(stocks)
merged_dict = {}
for key in base_info:
    merged_dict[key] = base_info[key]
    merged_dict[key]["bk"] = bk_info[key]
with open('full_data/base_data.json', 'w', encoding='utf-8') as f:
    json.dump(merged_dict, f, ensure_ascii=False, indent=4)