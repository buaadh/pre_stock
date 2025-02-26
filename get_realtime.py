from utils import *



#sina数据
df = ts.realtime_tick(ts_code='600000.SH')


#东财数据
df = ts.realtime_tick(ts_code='600000.SH', src='dc')
print(df)