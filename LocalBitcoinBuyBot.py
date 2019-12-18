import LocalBitcoin
import threading
from time import sleep

# Thread class to observe online buy ads
class LocalBitcoinBuyBot():
    def __init__(self):
        self.runningThread = None
        self.isRunning = False
        self.account_username = 'bengan59'
        self.auth_key = 'c210d587696cc6bbcfd302be02ee6127'
        self.auth_secret = '50c2267330b14f4f82832fb1836684cefc436063ec7db0c92c532ccf23a6fba0'
        self.higher_value = 1
        self.lowest_value = 7000
        self.highest_value = 8000
        self.country_code = 'se'
        self.country_name = 'sweden'
        self.payment_method = 'swish'
        self.refresh_interval = 10
        self.lcAgent = None

    def valueAcceptable(self, value):
        return value + self.higher_value <= self.highest_value

    # Get lowest online sell price
    def getOnlineHighestBuyPriceInUSD(self):
        onlineSellAds = self.lcAgent.getOnlineSellAds(self.country_code, self.country_name, self.payment_method)
        highest_value = 0
        highest_name = ''
        for ad in onlineSellAds['ad_list']:
            cur_value = ad['data']['temp_price_usd']
            cur_name = ad['data']['profile']['username']
            if (cur_name == self.account_username):
                continue
            if (float(cur_value) > highest_value):
                highest_value = float(cur_value)
                highest_name = ad['data']['profile']['username']
        print('buy highest ads ==> ', highest_name, highest_value)
        return {'value': highest_value, 'username': highest_name}

    # Update my ads' price equation to match the specified price
    def updateMyAdsPriceEquation(self, highest_name,  price_in_usd):
        my_ads = self.lcAgent.getOwnAds()

        for ad in my_ads['ad_list']:
            # filter ad which matches condition
            if (ad['data']['trade_type'] == 'ONLINE_BUY'
                    and self.changeToApiFormat(ad['data']['countrycode']) == self.country_code
                    and (self.changeToApiFormat(ad['data']['online_provider']) == self.payment_method
                         or (self.changeToApiFormat(ad['data']['online_provider']) == 'other' and self.payment_method == 'other-online-payment'))):
                # cur_price_in_usd = float(ad['data']['temp_price_usd']);
                # if (price_in_usd > cur_price_in_usd):       # only update when the new price is higher than my ads buy price
                # always update my ad into new price
                ad_id = ad['data']['ad_id']
                btc_in_usd = float(self.lcAgent.getBitcoinPrice('btc_in_usd'))
                margin = price_in_usd / btc_in_usd
                equation = 'btc_in_usd*USD_in_' + ad['data']['currency'] + '*' + str(margin)
                print('buy bot update ad ', ad_id, ' equation ', equation, ' value ', price_in_usd)
                self.lcAgent.updateAdsEquation(ad_id, equation)

    # thread run function
    def runFunc(self):
        while self.isRunning:
            try:
                highest_obj = self.getOnlineHighestBuyPriceInUSD()
                highest_value_in_usd = highest_obj['value']
                highest_name = highest_obj['username']
                if (self.valueAcceptable(highest_value_in_usd)):        # if lowest value is in range
                    specified_price = highest_value_in_usd + self.higher_value
                    print('buy update value acceptable! ', specified_price)
                    self.updateMyAdsPriceEquation(highest_name, specified_price)
                else:
                    print('buy update value unacceptable!')
            except Exception as e:
                print('buy bot runFunc exception ==> ', str(e))
            sleep(self.refresh_interval)

        self.lcAgent.logout()

    # change parameter format to matches the api format
    def changeToApiFormat(self, value):
        formatted_value = '-'
        pieces = value.lower().split()
        formatted_value = formatted_value.join(pieces)
        return formatted_value

    def start_thread(self, higher_value, lowest_value, highest_value, country_code, country_name, payment_method, auth_key, auth_secret, refresh_interval):
        self.higher_value = float(higher_value)
        self.lowest_value = float(lowest_value)
        self.highest_value = float(highest_value)
        self.country_code = self.changeToApiFormat(country_code)
        self.country_name = self.changeToApiFormat(country_name)
        self.payment_method = self.changeToApiFormat(payment_method)
        self.auth_key = auth_key
        self.auth_secret = auth_secret
        if (int(refresh_interval) > 0):
            self.refresh_interval = int(refresh_interval)
        else:
            self.refresh_interval = 10
        self.isRunning = True
        self.lcAgent = LocalBitcoin.LocalBitcoin(self.auth_key, self.auth_secret, True)
        self.runningThread = threading.Thread(target=self.runFunc)
        self.runningThread.start()
        print('buy bot thread started')

    def stop_thread(self):
        self.isRunning = False
        try:
            self.runningThread.join()
            del self.runningThread
            print('buy bot thread stopped')
        except:
            print('buy bot thread stop failed')
            pass
        del self.lcAgent
