import json
import pandas as pd
import time
import talib
from HuobiDMService import HuobiDM


def BuyK30(closed,ma3,rsi,macd,adx):
    position = 0
    priceD1 = 0
    step1 = False

    if ma3[-1]<ma3[-2]<ma3[-3] and ma3[-6]<ma3[-5]<ma3[-4]<ma3[-3]:
        priceD1 = max(closed[-6:-1])
        rsiD1 = max(rsi[-6:-1])
        macdD1 = max(macd[-6:-1])
        adxD1 = max(adx[-6:-1])
        if rsiD1 >70 and adxD1>30 and macdD1>1:
            for i in range(10, 200):
                if ma3[-i - 2] < ma3[-i - 1] < ma3[-i] and ma3[-i + 2] < ma3[-i + 1] < ma3[-i]:
                    priceD2 = max(closed[-i - 3:-i + 2])
                    macdD2 = max(macd[-i - 3:-i + 2])
                    if macdD2 > macdD1 and priceD2 < priceD1:
                        rsiD2 = max(rsi[-i - 3:-i + 2])
                        adxD2 = max(adx[-i - 3:-i + 2])
                        step1 = True
                        break
    if step1:
        position = 0.3
        if adxD2 > adxD1:
            position += 0.2
        if rsiD2 > rsiD1:
            position += 0.1

    return [position,priceD1]

def BuyK1(closed_1min):
    ma3 = talib.SMA(closed_1min, timeperiod=3)
    if ma3[-1] < ma3[-2] < ma3[-3] and ma3[-6] < ma3[-5] < ma3[-4] < ma3[-3]:
        return True
    return False


def BuyKoperation(account_info,position,closed_1min,priceD1):
    price = closed_1min[-1] * (1 - 0.001)
    margin_available_use = account_info['margin_available'] * position * 5 * (1 - 0.0003)
    volume_add = margin_available_use / price
    account_info['volume'] += volume_add
    account_info['margin_frozen'] += account_info['margin_available'] * position
    account_info['margin_available'] -= account_info['margin_available'] * position
    account_info['cost_price'] = closed_1min[-1]
    account_info['stop_price'] = min(priceD1*1.005,closed_1min[-1]*1.02)
    account_info['direction'] = 2
    # print('buy kong')

def SellKoperation(account_info,position,closed_1min):
    account_info['margin_available'] += account_info['margin_frozen'] * position
    account_info['margin_frozen'] -= account_info['margin_frozen'] * position
    account_info['margin_available'] -= account_info['volume'] * position * closed_1min[-1] * 0.001
    account_info['volume'] -= account_info['volume'] * position
    if position == 1:
        account_info['cost_price'] = 0
        account_info['direction'] = 0
        account_info['stop_price'] = 0


def reduceStop_priceK(account_info,closed,highed):
    ma5 = talib.SMA(closed, timeperiod=5)
    if ma5[-1]<ma5[-2]<ma5[-3] and ma5[-6]<ma5[-5]<ma5[-4]<ma5[-3]:
        holdPlace = max(highed[-6:-1])
        if holdPlace < account_info['stop_price'] * 0.99:
            account_info['stop_price'] = holdPlace


def SellK30(closed,ma3,macd):
    position = 0
    if ma3[-1] > ma3[-2] > ma3[-3] and ma3[-6] > ma3[-5] > ma3[-4] > ma3[-3]:
        priceD1 = min(closed[-6:-1])
        macdD1 = min(macd[-6:-1])
        for i in range(8, 100):
            if ma3[-i - 2] > ma3[-i - 1] > ma3[-i] and ma3[-i + 2] > ma3[-i + 1] > ma3[-i]:
                priceD2 = min(closed[-i - 3:-i + 2])
                macdD2 = min(macd[-i - 3:-i + 2])
                if macdD2<macdD1 and priceD2>priceD1:
                    return 1
    return position

def StopK1(account_info,closed_1min):
    if closed_1min[-1]>account_info['stop_price']:
        return True
    return False


def SellK1(closed_1min):
    ma3 = talib.SMA(closed_1min, timeperiod=3)
    if ma3[-1] > ma3[-2] > ma3[-3] and ma3[-6] > ma3[-5] > ma3[-4] > ma3[-3]:
        return True
    return False


def BuyD30(closed,lowed,rsi,ma60):
    position = 0
    priceD1 = 0
    priceD2 = 0
    ma5 = talib.SMA(lowed, timeperiod=5)
    if closed[-1]>ma60[-1]:
        return [0,0,0]
    if ma5[-1] > ma5[-2] > ma5[-3] and ma5[-7] > ma5[-6] > ma5[-5] > ma5[-4] > ma5[-3]:
        priceD1 = min(closed[-6:-1])
        for i in range(10, 100):
            if closed[-i]>ma60[-i]:
                return [0,0,0]
            if ma5[-i - 4] > ma5[-i - 3] >ma5[-i - 2] > ma5[-i - 1] > ma5[-i] and ma5[-i + 3] > ma5[-i + 2] > ma5[-i + 1] > ma5[-i]:
                priceD2 = min(closed[-i - 3:-i + 2])
                rsiD2 = min(rsi[-i - 3:-i + 2])
                if rsiD2<30 and priceD1>priceD2:
                    position =0.5
                break
    return [position,priceD1,priceD2]

def BuyD1(closed_1min):
    ma3 = talib.SMA(closed_1min, timeperiod=3)
    if ma3[-1] > ma3[-2] > ma3[-3] and ma3[-6] > ma3[-5] > ma3[-4] > ma3[-3]:
        return True
    return False

def BuyDoperation(account_info,position,closed_1min,priceD1,priceD2):
    price = closed_1min[-1] * 1.001
    margin_available_use = account_info['margin_available'] * position * 5 * (1 - 0.0003)
    volume_add = margin_available_use / price
    account_info['volume'] += volume_add
    account_info['margin_frozen'] += account_info['margin_available'] * position
    account_info['margin_available'] -= account_info['margin_available'] * position
    if account_info['direction']==0:
        account_info['cost_price'] = closed_1min[-1]* 0.98
        account_info['stop_price'] = max(priceD2, priceD1* 0.99)
        account_info['direction'] = 1
        account_info['first_buy'] = 1


def SellDoperation(account_info,position,closed_1min):
    account_info['margin_available'] += account_info['margin_frozen'] * position
    account_info['margin_frozen'] -= account_info['margin_frozen'] * position
    account_info['margin_available'] -= account_info['volume'] * position * closed_1min[-1] * 0.001
    account_info['volume'] -= account_info['volume'] * position
    if position == 1:
        account_info['cost_price'] = 0
        account_info['stop_price'] = 0
        account_info['direction'] = 0
        account_info['first_buy'] = 0



def addStop_priceD(account_info,closed,lowed):
    ma5 = talib.SMA(closed, timeperiod=5)
    if ma5[-1]>ma5[-2]>ma5[-3] and ma5[-6]>ma5[-5]>ma5[-4]>ma5[-3]:
        holdPlace = min(lowed[-6:-1])
        if account_info['stop_price']==0 or holdPlace > account_info['stop_price'] * 1.02:
            account_info['stop_price'] = holdPlace



def addCost_priceD(account_info, closed, lowed):
    position = 0
    ma5 = talib.SMA(closed, timeperiod=5)
    if ma5[-1] > ma5[-2] > ma5[-3] and  ma5[-5] > ma5[-4] > ma5[-3]:
        holdPlace = min(lowed[-6:-1])
        if holdPlace > account_info['cost_price'] * 1.03 and account_info['first_buy'] == 1:
            position = 0.3
            account_info['cost_price'] = account_info['cost_price'] * 1.03
            account_info['first_buy'] = 2
    return position



def SellD30(closed,ma3,ma60,rsi,macd,adx,account_info):
    position = 0

    if ma3[-1]<ma3[-2] and max(rsi[-3:])>80 and max(rsi[-3:])>rsi[-1]:
        position = max(position,0.5)

    if ma3[-1]<ma60[-1] and ma3[-2]>=ma60[-2]:
        position = max(position,1)


    if ma3[-1] < ma3[-2] < ma3[-3] and ma3[-5] < ma3[-4] < ma3[-3]:
        priceD1 = max(closed[-6:-1])
        macdD1 = max(macd[-6:-1])
        adxD1 = max(adx[-6:-1])
        if adxD1 > 30 and macdD1 > 1:
            for i in range(10, 200):
                if ma3[-i - 2] < ma3[-i - 1] < ma3[-i] and ma3[-i + 2] < ma3[-i + 1] < ma3[-i]:
                    priceD2 = max(closed[-i - 3:-i + 2])
                    macdD2 = max(macd[-i - 3:-i + 2])
                    adxD2 = max(adx[-i - 3:-i + 2])
                    if macdD2 > macdD1 and priceD2 < priceD1 and adxD2>adxD1:
                        position = max(position,1)
                        break

    if closed[-1]<account_info['stop_price']:
        position = max(position, 0.5)
        account_info['stop_price'] = 0


    return position


def StopD1(account_info,closed_1min):
    if closed_1min[-1]<=account_info['cost_price']:
        return True
    return False

def SellD1(closed_1min):
    ma3 = talib.SMA(closed_1min, timeperiod=3)
    if ma3[-1] < ma3[-2] < ma3[-3] and ma3[-6] < ma3[-5] < ma3[-4] < ma3[-3]:
        return True
    return False


with open("test_account_info.json", 'r') as load_f:
    account_info = json.load(load_f)

URL = 'https://www.hbdm.com/'
ACCESS_KEY = ''
SECRET_KEY = ''
count = 0
retryCount =0

id_30 =0
positionBuyD = 0
positionSellD = 0
positionBuyK = 0
positionSellK = 0
priceD1=0
priceD2=0

priceKD=0

while (1):
    try:
        dm = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)
        kline_1min = (dm.get_contract_kline(symbol='ETH_CQ', period='1min'))['data']
        kline_30min = (dm.get_contract_kline(symbol='ETH_CQ', period='30min',size=360))['data']
    except:
        retryCount += 1
        if(retryCount == 20):
            with open("test_account_info.json", "w") as dump_f:
                json.dump(account_info, dump_f)
            print('connect ws error!')
            break
        continue

    retryCount=0

    kline_1 = (pd.DataFrame.from_dict(kline_1min))[['id', 'close', 'high', 'low', 'open', 'amount']]
    closed_1 = kline_1['close'].values
    opened_1 = kline_1['open'].values
    highed_1 = kline_1['high'].values
    lowed_1 = kline_1['low'].values


    if account_info['direction'] == 2:
        if (account_info['margin_available'] + account_info['margin_frozen'] +
            (account_info['price'] - highed_1[-1]) * account_info['volume']) <= 0:
            account_info['margin_available'] = 0
            account_info['margin_frozen'] = 0
            account_info['cost_price'] = 0
            account_info['volume'] = 0
            account_info['direction'] =0
        account_info['margin_available'] += (account_info['price'] - closed_1[-1]) * account_info['volume']
    elif account_info['direction'] == 1:
        if (account_info['margin_available'] + account_info['margin_frozen'] +
            (lowed_1[-1] - account_info['price']) * account_info['volume']) <= 0:
            account_info['margin_available'] = 0
            account_info['margin_frozen'] = 0
            account_info['cost_price'] = 0
            account_info['volume'] = 0
            account_info['direction'] = 0
        account_info['margin_available'] += (closed_1[-1] - account_info['price']) * account_info['volume']

    account_info['price'] = closed_1[-1]

    if account_info['direction'] == 1 and StopD1(account_info, closed_1):
        SellDoperation(account_info, 1, closed_1)
        print('sell D')
        print(id_30)
        positionBuyD = 0
        positionSellD = 0


    if account_info['direction'] == 2 and StopK1(account_info, closed_1):
        SellKoperation(account_info, 1, closed_1)
        print('sell K')
        print(id_30)
        positionBuyK = 0
        positionSellK = 0

    if positionBuyD>0 and BuyD1(closed_1):
        if account_info['direction'] == 2:
            SellKoperation(account_info, 1, closed_1)
            print('sell K')
            print(id_30)
            positionBuyK = 0
            positionSellK = 0
        BuyDoperation(account_info, positionBuyD, closed_1, priceD1, priceD2)
        print('buy D')
        print(id_30)
        positionBuyD = 0

    if positionSellD>0 and SellD1(closed_1):
        SellDoperation(account_info, positionSellD, closed_1)
        print('sell D')
        print(id_30)
        positionBuyD = 0
        positionSellD = 0

    if positionBuyK>0 and BuyK1(closed_1):
        if account_info['direction'] == 1:
            SellDoperation(account_info, 1, closed_1)
            positionBuyD = 0
            positionSellD = 0
        BuyKoperation(account_info, positionBuyK, closed_1, priceKD)
        print('buy K')
        print(id_30)
        positionBuyK = 0

    if positionSellK>0 and SellK1(closed_1):
        SellKoperation(account_info, positionSellK, closed_1)
        print('sell K')
        print(id_30)
        positionBuyK = 0
        positionSellK = 0


    kline_30 = (pd.DataFrame.from_dict(kline_30min))[['id', 'close', 'high', 'low', 'open', 'amount']]
    id = kline_30['id'].values
    id = (id[-1] / 1800)
    if id >id_30:
        id_30 = id

        closed = kline_30['close'].values
        closed = closed[:-1]
        opened = kline_30['open'].values
        opened = opened[:-1]
        highed = kline_30['high'].values
        highed = highed[:-1]
        lowed = kline_30['low'].values
        lowed = lowed[:-1]

        ma3 = talib.SMA(closed, timeperiod=3)
        ma60 = talib.SMA(closed, timeperiod=60)
        rsi = talib.RSI(closed, timeperiod=14)
        macd, signal, hist = talib.MACD(closed, fastperiod=12, slowperiod=26, signalperiod=9)
        adx = talib.ADX(highed, lowed, closed, timeperiod=12)

        if account_info['direction'] == 1:
            addStop_priceD(account_info, closed, lowed)
            positionBuyD = addCost_priceD(account_info, closed, lowed)
            positionSellD = SellD30(closed, ma3, ma60, rsi, macd, adx, account_info)


        if account_info['direction'] == 2:
            reduceStop_priceK(account_info, closed, highed)
            positionSellK = SellK30(closed, ma3, macd)


        [positionBuyK, priceKD] = BuyK30(closed, ma3, rsi, macd, adx)

        [positionBuyD, priceD1, priceD2] = BuyD30(closed, lowed, rsi, ma60)



    count +=1

    if(count%200==0):
        print(account_info['margin_available'] + account_info['margin_frozen'])

    time.sleep(10)
