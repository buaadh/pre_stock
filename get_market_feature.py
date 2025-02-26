from utils import *



def get_market_index(start_date, end_date):
    market_index = {}
    shen_index = ak.index_hist_cni(symbol="399001", start_date=start_date, end_date=end_date)
    market_index["shen_index"] = df2dict(shen_index)
    concepts = [
            "标准普尔",
            "富时罗素",
            "MSCI中国",
            "沪股通",
            "中证500",
            "国企改革",
            "粤港自贸",
            "融资融券",
            "预盈预增",
            "机构重仓"
        ]
    for concept in tqdm(concepts,'loading concepts index'):
        stock_board_concept_hist_em_df = ak.stock_board_concept_hist_em(symbol=concept, period="daily", start_date=start_date, end_date=end_date, adjust="")
        market_index[concept] = df2dict(stock_board_concept_hist_em_df)
    return market_index
