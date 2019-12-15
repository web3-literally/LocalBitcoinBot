import LocalBitcoin
import threading
from time import sleep

# Thread class to observe online buy ads
class LocalBitcoinSellBot():
    def __init__(self):
        self.runningThread = None
        self.isRunning = False
        self.account_username = 'bengan59'
        self.auth_key = '1b33c78346dcb50e37a5c7f0672db14f'
        self.auth_secret = 'f1a2adcf3accce3d6bec25272320f8ac568991d4866ecfbd74f25d8c343760dc'
        self.lower_value = 1
        self.lowest_value = 7000
        self.highest_value = 8000
        self.country_code = 'se'
        self.country_name = 'sweden'
        self.payment_method = 'swish'
        self.refresh_interval = 10
        self.lcAgent = None

    def valueAcceptable(self, value):
        return value >= self.lowest_value + self.lower_value

    # Get lowest online sell price
    def getOnlineLowestSellPriceInUSD(self):
        onlineBuyAds = self.lcAgent.getOnlineBuyAds(self.country_code, self.country_name, self.payment_method)
        lowest_value = 9999999
        lowest_name = ''
        for ad in onlineBuyAds['ad_list']:
            cur_value = ad['data']['temp_price_usd']
            cur_name = ad['data']['profile']['username']
            if (cur_name == self.account_username):
                continue
            if (float(cur_value) < lowest_value):
                lowest_value = float(cur_value)
                lowest_name = ad['data']['profile']['username']
        print('sell lowest ads ==> ', lowest_name, lowest_value)
        return {'value': lowest_value, 'username': lowest_name}

    # Update my ads' price equation to match the specified price
    def updateMyAdsPriceEquation(self, lowest_name,  price_in_usd):
        my_ads = self.lcAgent.getOwnAds()

        for ad in my_ads['ad_list']:
            # filter ad which matches condition
            if (ad['data']['trade_type'] == 'ONLINE_SELL'
                    and self.changeToApiFormat(ad['data']['countrycode']) == self.country_code
                    and self.changeToApiFormat(ad['data']['online_provider']) == self.payment_method):
                # cur_price_in_usd = float(ad['data']['temp_price_usd']);
                # if (price_in_usd < cur_price_in_usd):       # only update when the new price is lower than my ads sell price
                # always update my ad into new price
                ad_id = ad['data']['ad_id']
                btc_in_usd = float(self.lcAgent.getBitcoinPrice('btc_in_usd'))
                margin = price_in_usd / btc_in_usd
                equation = 'btc_in_usd*USD_in_' + ad['data']['currency'] + '*' + str(margin)
                print('sell bot update ad ', ad_id, ' equation ', equation, ' value ', price_in_usd)
                self.lcAgent.updateAdsEquation(ad_id, equation)

    # thread run function
    def runFunc(self):
        while self.isRunning:
            try:
                lowest_obj = self.getOnlineLowestSellPriceInUSD()
                lowest_value_in_usd = lowest_obj['value']
                lowest_name = lowest_obj['username']
                if (self.valueAcceptable(lowest_value_in_usd)):        # if lowest value is in range
                    specified_price = lowest_value_in_usd - self.lower_value
                    print('sell update value acceptable! ', specified_price)
                    self.updateMyAdsPriceEquation(lowest_name, specified_price)
                else:
                    print('sell update value unacceptable!')
            except Exception as e:
                print('sell bot runFunc exception ==> ', str(e))
            sleep(self.refresh_interval)

        self.lcAgent.logout()

    # change parameter format to matches the api format
    def changeToApiFormat(self, value):
        formatted_value = '-'
        pieces = value.lower().split()
        formatted_value = formatted_value.join(pieces)
        return formatted_value

    def start_thread(self, lower_value, lowest_value, highest_value, country_code, country_name, payment_method, auth_key, auth_secret, refresh_interval):
        self.lower_value = float(lower_value)
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
        self.lcAgent = LocalBitcoin.LocalBitcoin(self.auth_key, self.auth_secret, False)
        self.runningThread = threading.Thread(target=self.runFunc)
        self.runningThread.start()
        print('sell bot thread started')

    def stop_thread(self):
        self.isRunning = False
        try:
            self.runningThread.join()
            del self.runningThread
            print('sell bot thread stopped')
        except:
            print('sell bot thread stop failed')
            pass
        del self.lcAgent
