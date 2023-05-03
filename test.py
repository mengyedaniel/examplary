import os
import pandas as pd

category='milk'

path = '/~/'

os.chdir(path)

fs = os.listdir()
fs =[i for i in fs if i[:6]>="202201"]
fs =[i for i in fs if not i.startswith("o")]
fs.sort()
print(fs)


ls = []
for i in fs:
    tmp = pd.read_csv(i, encoding='gb18030')
    ls.append(tmp)
d_out = pd.concat(ls)

d_out['month'] = d_out['period'].apply(lambda x: x[:7])
d_out.loc[d_out['period']=="2022-07-02", 'month'] = "2022-06"

def func(x):
    if x<10000:
        return "a_<1w"
    elif x<100000:
        return "b_<10w"
    else:
        return "c_10w+"

d_out['tag'] = d_out['sales_unit_this_t'].apply(lambda x: func(x))
d_out['s_v'] = d_out['sales_unit_inc_pred'] * d_out['group_price']

aa = d_out.groupby(['month','tag']).agg({'s_v':'sum','goods_id':'count'})
bb = d_out.groupby(['month','tag']).agg({'s_v':'sum','goods_id':'count'}).apply(lambda x: x/x.groupby(level=0).sum())
cc = d_out.query('tag!="a_<1w" and sales_unit_inc!=sales_unit_inc_pred and sales_unit_inc_pred!=comments_cnt').groupby(['month','tag']).agg({'s_v':'sum','goods_id':'count'})
dd = d_out.query('tag!="a_<1w" and sales_unit_inc!=sales_unit_inc_pred and sales_unit_inc_pred==comments_cnt').groupby(['month','tag']).agg({'s_v':'sum','goods_id':'count'})


aa.rename(columns = {"s_v":"sales_value", "goods_id":"item_cnt"}, inplace=True)
bb.rename(columns = {"s_v":"sales_value_prop", "goods_id":"item_cnt_prop"}, inplace=True)
cc.rename(columns = {"s_v":"stock_sales_proj", "goods_id":"stock_proj_item_cnt"}, inplace=True)
dd.rename(columns = {"s_v":"comments_sales_proj","goods_id":"comments_proj_item_cnt"}, inplace=True)


output = pd.concat([aa,bb,cc,dd], axis=1)
output['categ'] = category
output.to_csv('/~/' +category +'_share_0803.csv')
print('done')