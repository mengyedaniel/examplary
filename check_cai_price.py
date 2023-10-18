#装载相关的package
import pandas as pd
import datetime

#品牌名和文件名中缩写的对应
brand_map = {
    "Continental":"CO",
    "Michelin":"MI",
    "Bridgestone":"BS",
    "Goodyear":"GO",
    "Dunlop":"DU",
    "Hankook":"HK",
}

#获取日期
today = datetime.date.today()
first = today.replace(day=1)
this_month = first.strftime("%Y%m%d")
last_month = (first - datetime.timedelta(days=1)).replace(day=1).strftime("%Y%m%d")


def check_cai_price(brand, month_l = last_month, month_r = this_month, threshold=0.08, savefile=True):
    brand_acronym = brand_map[brand]
    path_l = 'Template_{}_CN_TC_{}.xlsx'.format(brand_acronym, month_l)
    path_r = 'Template_{}_CN_TC_{}.xlsx'.format(brand_acronym, month_r)
   
    #读取文件左表df_l为上月，右表df_r为本月
    df_l = pd.read_excel(path_l)
    df_r = pd.read_excel(path_r)
   
    #修改列名，全部改成小写，方便后续引用
    df_l.columns = [i.lower() for i in df_l.columns] 
    df_r.columns = [i.lower() for i in df_r.columns]


    df_l['list_price_l'] = df_l.groupby('cai')['retailer si list price'].transform('min')
    df_l['net_price_l'] = df_l.groupby('cai')['monthly retailer net sell-in price,conditional'].transform('min')

    df_r['list_price_r'] = df_r.groupby('cai')['retailer si list price'].transform('min')
    df_r['net_price_r'] = df_r.groupby('cai')['monthly retailer net sell-in price,conditional'].transform('min')

    #将左表和右表按照CAI做join，方式为取并集，同时标注是左表特有，交叉，右表特有
    df_merg = pd.merge(df_l,df_r, on='cai', how='outer', indicator=True) #

    #计算net price gap = 右表net price（当月）/左表net price(上月) - 1
    df_merg['net_price_gap'] = df_merg['net_price_r']/df_merg['net_price_l']-1
    #生成net price gap绝对值大于等于threshold的标签，默认值0.08
    df_merg['p_tag'] = df_merg['net_price_gap'].apply(lambda x: abs(x)>=threshold)
    #交叉行数，左表特有行数，右表特有行数计数
    overlap_rows, left_only_rows, right_only_rows = df_merg['_merge'].value_counts()
    #打印以上行数
    print('\n', month_l,"&",month_r,"overlap rows:", overlap_rows,'\n',
          month_l, " ", brand, " ", "rows:",left_only_rows + overlap_rows, '\n',
          month_r, " ", brand, " ", "rows:", right_only_rows + overlap_rows,'\n',
          ' ')
    #打印各部分的比例
    print(df_merg['_merge'].value_counts()/df_merg.shape[0])

    #取p_tag为True的行数，且为两月都出现的CAI
    out = df_merg.query('p_tag==True and _merge=="both"')[['cai',
                    'dimbox_x',
                    'net_price_gap',
                    'net_price_l',
                    'net_price_r',
                    'list_price_l',
                    'list_price_r']]

    #修改列名
    out.rename(columns = {'net_price_l' : "net_{}".format(month_l),
                'net_price_r' : "net_{}".format(month_r),
                'list_price_l': "list_{}".format(month_l),
                'list_price_r': "list_{}".format(month_r),
                'dimbox_x':"dimbox"                        
                            }, inplace=True)
    
    #是否存储文件，默认为是
    if savefile:
        out.to_excel(month_r + ' ' + brand + 'cai_price_gap.xlsx', index=False)
  
    return out