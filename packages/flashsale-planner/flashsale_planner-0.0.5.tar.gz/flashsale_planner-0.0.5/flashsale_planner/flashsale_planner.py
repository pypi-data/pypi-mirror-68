import requests
import pickle
import pandas as pd
import numpy as np
from datetime import date
from itertools import product

dummies = [
    'brand','product_show_shopee_verified_label','shop_account_email_verified',
    'flash_bin','product_parent_catid'
]
numerics = [
    'flash_sale_stock','price_before_discount','price',
    'discount','product_liked_count','product_historical_sold',
    'product_star','shop_rating_bad','shop_rating_normal',
    'shop_rating_good','shop_follower_count','shop_item_count',
    'shop_response_rate','shop_response_rate_null','shop_cancellation_rate',
    'shop_account_total_avg_star','shop_account_total_avg_star_null','shop_age'
]

def _get_item(itemid,shopid):
    url = f'https://shopee.co.th/api/v2/item/get?itemid={itemid}&shopid={shopid}'
    response = requests.get(url)
    return response.json()

def _get_shop(shopid):
    url = f'https://shopee.co.th/api/v2/shop/get?shopid={shopid}'
    response = requests.get(url)
    return response.json()

def _get_item_features(itemid,shopid):
    data = _get_item(itemid,shopid)
    item = data['item']
    include = {
        'price_min_before_discount',
        'price_before_discount',
        'price_max_before_discount',
        'price_min',
        'price_max',
        'price',
        'raw_discount',
        'liked_count',
        'historical_sold',
        'brand',
        'categories',
        'show_shopee_verified_label',
        'item_rating'}
    item = {feature: item[feature] for feature in item if feature in include}
    catids = [
        'parent_catid',
        'catid',
        'sub_catid']
    cats = [
        'parent_cat',
        'cat',
        'sub_cat']
    for category,catid,cat in zip(item['categories'],catids,cats):
        item[catid] = category['catid']
        item[cat] = category['display_name']
    del item['categories']
    for feature in item['item_rating']:
        item[feature] = item['item_rating'][feature]
    del item['item_rating']
    counts = [
        'total_rating',
        'star_1',
        'star_2',
        'star_3',
        'star_4',
        'star_5']
    for number,count in zip(item['rating_count'],counts):
        item[count] = number
    del item['rating_count']
    item = {'product_'+feature: item[feature] for feature in item}
    return item
        
def _get_shop_features(shopid):
    data = _get_shop(shopid)
    shop = data['data']
    include = {
        'ctime',
        'rating_bad',
        'rating_normal',
        'rating_good',
        'follower_count',
        'item_count',
        'shop_location',
        'account',
        'response_rate',
        'cancellation_rate',
        'disable_make_offer',
        'name',
        'rating_star'}
    account_features = {
        'username',
        'following_count',
        'email_verified',
        'fbid',
        'total_avg_star',
        'phone_verified',
        'is_seller'}
    shop = {feature: shop[feature] for feature in shop if feature in include}
    for feature in shop['account']:
        if feature in account_features:
            shop['account_'+feature] = shop['account'][feature]
    del shop['account']
    shop = {'shop_'+feature: shop[feature] for feature in shop}
    return shop

def _clean(df):
    today = date.today()

    df['price'] = (1-df.discount)*df.price_before_discount
    df['discount_price'] = df.price_before_discount-df.price
    df['shop_response_rate'] /= 100
    df['shop_cancellation_rate'] /= 100
    df['brand'] = pd.Categorical((~(df['product_brand'].str.lower().str.contains('no brand') | \
        df['product_brand'].str.contains('ไม่มียี่ห้อ') | \
        df['product_brand'].str.contains('ไม่มีแบรนด์') | \
        df['product_brand'].str.lower().str.contains('no name') | \
        df['product_brand'].str.contains('โนเนม') | \
        df['product_brand'].isin(['None','0','']))).astype(int),[0,1])
    df['shop_account_total_avg_star_null'] = pd.Categorical(df['shop_account_total_avg_star'].isna().astype(int),[0,1])
    df['shop_account_total_avg_star'].fillna(0,inplace=True)
    df['shop_response_rate_null'] = pd.Categorical(df['shop_response_rate'].isna().astype(int),[0,1])
    df['shop_response_rate'].fillna(0,inplace=True)
    df['flash_bin'] = df['flash_bin'].str.replace('-','_')
    df['flash_bin'] = pd.Categorical(df['flash_bin'],categories['flash_bin'])
    df['product_parent_catid'] = df['product_parent_catid'].astype(int)
    df['product_parent_catid'] = pd.Categorical(df['product_parent_catid'],categories['product_parent_catid'])
    df['product_show_shopee_verified_label'] = pd.Categorical(df['product_show_shopee_verified_label'].astype(int),[0,1])
    df['shop_account_email_verified'] = pd.Categorical(df['shop_account_email_verified'].astype(int),[0,1])
    df['product_star'] = np.where(
        df.loc[:,df.columns.str.startswith('product_star')].sum(axis=1) == 0,0,
        (df.loc[:,df.columns.str.startswith('product_star')]*np.array([1,2,3,4,5])).sum(axis=1)/df.loc[:,df.columns.str.startswith('product_star')].sum(axis=1))
    df['shop_age'] = df.shop_ctime.map(lambda x: (pd.to_datetime(today)-pd.to_datetime(x*1e9)).days)
    df = df[df[dummies+numerics].notnull().all(axis=1)]
    df = pd.get_dummies(df[dummies+numerics],columns=dummies)
    return df

def _get_preprocessing(project):
    url = f'https://us-central1-{project}.cloudfunctions.net/get_preprocessing'
    response = requests.get(url)
    return pickle.loads(response.content)

def _get_classifier(project):
    url = f'https://us-central1-{project}.cloudfunctions.net/get_classifier'
    response = requests.get(url)
    return pickle.loads(response.content)

def _get_regressor(project):
    url = f'https://us-central1-{project}.cloudfunctions.net/get_regressor'
    response = requests.get(url)
    return pickle.loads(response.content)

def initialize(project='datasciprac'):
    global poly,scaler,categories,features,model_hgb_clf,model_hgb_reg
    preprocessing = _get_preprocessing(project)
    clf = _get_classifier(project)
    reg = _get_regressor(project)

    poly = preprocessing['poly']
    scaler = preprocessing['scaler']
    categories = preprocessing['categories']
    features = preprocessing['features']

    model_hgb_clf = clf['model_hgb']

    model_hgb_reg = reg['model_hgb']

def predict(itemid,shopid,flash_sale_stock,discount,price_before_discount,flash_bin=['0-12','12-18','18-21','21-24'],sold_out_threshold=.7):
    if not(isinstance(flash_bin,str) or all(isinstance(x,str) for x in flash_bin)):
        return None
    if not(isinstance(itemid,(int,np.integer)) and isinstance(shopid,(int,np.integer))):
        print('itemid or shopid')
        return None
    if not(isinstance(flash_sale_stock,(int,np.integer)) or all(isinstance(x,(int,np.integer)) for x in flash_sale_stock)):
        print('flash_sale_stock')
        return None
    if not(isinstance(discount,(int,np.integer,float,np.floating)) or all(isinstance(x,(int,np.integer,float,np.floating)) for x in discount)):
        print('discount')
        return None
    if not(isinstance(price_before_discount,(int,np.integer,float,np.floating)) or all(isinstance(x,(int,np.integer,float,np.floating)) for x in price_before_discount)):
        print('price_before_discount')
        return None
    if isinstance(flash_bin,str):
        flash_bin = [flash_bin]
    if isinstance(flash_sale_stock,int):
        flash_sale_stock = [flash_sale_stock]
    if isinstance(discount,(int,float)):
        discount = [discount]
    if isinstance(price_before_discount,(int,float)):
        price_before_discount = [price_before_discount]

    flash_sale = pd.DataFrame(
        product(flash_bin,flash_sale_stock,discount,price_before_discount),
        columns=['flash_bin','flash_sale_stock','discount','price_before_discount']).to_dict(orient='list')
    item = _get_item_features(itemid,shopid)
    shop = _get_shop_features(shopid)
    data = pd.DataFrame({**flash_sale,**item,**shop})
    data = _clean(data)
    data = pd.DataFrame(poly.transform(data),columns=poly.get_feature_names(data.columns))
    data = data[features]
    data = pd.DataFrame(scaler.transform(data),columns=data.columns)
    sold_out = model_hgb_clf.predict_proba(data).T[1] > sold_out_threshold
    sold_out_prob = model_hgb_clf.predict_proba(data).T[1]
    sold_rate = model_hgb_reg.predict(data)
    prediction = pd.DataFrame(
        {**flash_sale,**{'sold_out': sold_out,'sold_out_prob': sold_out_prob,'sold_rate': sold_rate}})
    prediction['revenue'] = np.where(prediction.sold_out,
                                     prediction.flash_sale_stock*prediction.price_before_discount*prediction.discount,
                                     prediction.flash_sale_stock*prediction.price_before_discount*prediction.discount*prediction.sold_rate)
    return prediction