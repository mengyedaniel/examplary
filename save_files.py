import pandas as pd
import os

f_ls = os.listdir('/~/')



m = "202208"



#p_dt = pd.read_csv('/~.csv', encoding='gb18030')
#p_dt = p_dt[['PROD_ID','ATTRIBUTE']].set_index('PROD_ID').to_dict()['ATTRIBUTE']


if not os.path.exists('/~/{}'.format(m)):
    os.makedirs('/~/{}'.format(m))


f_sub = [i for i in f_ls if i.endswith('{}.csv'.format(m))]
print(f_sub)
a=0
for i in f_sub:
    tmp = pd.read_csv(i, encoding='utf-8')
    a+=tmp.shape[0]
    tmp.rename(columns={'BERT':'CATCODE','price_adj':'adj_price'}, inplace=True)
    
    #tmp['prod_info'] = tmp['goods_id'].map(p_dt)
    #tmp.loc[tmp.property_info.isnull(), 'property_info'] = tmp[tmp.property_info.isnull()]['prod_info']   
    
    tmp = tmp[['period','goods_id','opt_1_name','opt_2_name','opt_3_name','mall_id','mall_name','brand_name','PROD_DESC_RAW','CATCODE','sales_unit_adj','adj_price','price_disc_adj','comments_cnt','store_type','merchant_type','property_info']]

    tmp.sales_unit_adj.fillna(0, inplace=True)
    
    tmp.to_csv('/~/{}/{}.csv'.format(m,i[:i.rfind('_')]), encoding='utf-8',index=False)
    print(i[:i.rfind('_')])
    print(tmp.period.unique())
        

ls = []
fs = os.listdir('/~/')

fs = [i for i in fs if i[3:9]==m]
print(fs)
for f in fs:
    tmp = pd.read_csv('/~/'+ f, encoding='utf-8')
    ls.append(tmp)
df=pd.concat(ls)

df = df.query('BERT not in ["IMF","DIAP","COFF","SP","WHISK","DWL","BATHROOMT","FACIALT","LAUND","MILK"] and period!="2022-07-02"')
df.rename(columns={'BERT':'CATCODE','sales_unit_inc':'sales_unit','group_price':'price'}, inplace=True)

df['store_type'] = ''
df.loc[df.merchant_type.isin([3,4,5]), 'store_type'] = 'b'
df.store_type.replace({'':'c'}, inplace=True)

#df['prod_info'] = df['goods_id'].map(p_dt)
#df.loc[df.property_info.isnull(), 'property_info'] = df[df.property_info.isnull()]['prod_info']

df =df[['period','goods_id','opt_1_name','opt_2_name','opt_3_name','mall_id','mall_name','brand_name','PROD_DESC_RAW','CATCODE','sales_unit','price','discount_price','comments_cnt','store_type','merchant_type','property_info']]

df.sales_unit.fillna(0, inplace=True)


print(df.period.unique())
print(a)
df.to_csv('/~/{}/OTHERS.csv'.format(m), encoding='utf-8', index=False)
