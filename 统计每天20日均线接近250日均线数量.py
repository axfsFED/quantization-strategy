'''
个股均线收敛统计
'''
# 导入函数库
import datetime,time,calendar
import numpy as np
import pandas as pd
import math

test_ma_length_up = 20

"this is the change"
 
start_date = '2017-8-1'
end_date = '2017-9-1'

# 字符串，提示信息
cols = ['日期', '满足条件股票数量', '全体A股数量']
file_name = '统计.csv'

# 存放满足条件的股票明细数据
global df_array
df_array = []

# 当前日期向前追溯或向后推进months月份，Python2下正常运行
def date_window(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day,calendar.monthrange(year,month)[1])
    dt = dt.replace(year=year, month=month, day=day)
    return dt
    
# 每天要执行的函数, 统计当天所有满足条件的股票
def handle_data(date): 
    temp = []
    # 获取当天所有A股数据
    securities = list(get_all_securities(['stock'],date).index)
    today = datetime.datetime.strptime(str(date),'%Y-%m-%d')
    ma_length_max = max(test_ma_length_up, test_ma_length_down)

    all_securities_num = 0
    the_securities_num = 0

    for security in securities:
        df_info = get_price(security, end_date=date, count=1, fields=['paused'], skip_paused=False, fq='pre')
        is_paused = df_info['paused'][0] #判断当天是否停牌
        if is_paused: # 判断停牌
            continue
			
        df_info = get_price(security, end_date=date, count=ma_length_max, fields=['close'], skip_paused=False, fq='pre')
        if isnan(df_info.iloc[0].iloc[0]):
            continue
        all_securities_num += 1
        ma_up = sum(df_info[-test_ma_length_up:]).iloc[0]/test_ma_length_up
        ma_down = sum(df_info[-test_ma_length_down:]).iloc[0]/test_ma_length_down
        
        if (ma_up-ma_down)/ma_down > -0.01:
            the_securities_num += 1

    temp.append(date)
    temp.append(the_securities_num)
    temp.append(all_securities_num)
    df_array.append(temp)

if __name__ == '__main__':
    start_time = datetime.datetime.now()

    trade_days = jqdata.get_trade_days(start_date=start_date, end_date=end_date)
    if len(trade_days) == 0:
        print("所选日期范围无交易日，请重新选择")
    else:
        for day in trade_days:
            print(day)
            handle_data(day)
        # 将每日计算数据存入DataFrame, 并写入CSV文件
        df = pd.DataFrame(df_array, index=range(len(df_array)), columns=cols)
        write_file(file_name, df.to_csv(), append=False)
        print("统计结束！")

        end_time = datetime.datetime.now()
        print('执行时间:%s s'%(end_time - start_time).seconds)