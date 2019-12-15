
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from LocalBitcoinBuyBot import LocalBitcoinBuyBot
from LocalBitcoinSellBot import LocalBitcoinSellBot

# Bot thread
gbuyBot = None
gsellBot = None

# Main window to show setting page
class MainWnd(QMainWindow):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        # Implememt GUI
        self.initUI()

    # Init UI
    def initUI(self):
        layout = QVBoxLayout()

        buyBotUI = self.initBuyBotUI()
        sellBotUI = self.initSellBotUI()

        lay_hor_interval = QHBoxLayout()
        refresh_interval_label = QLabel('Refresh Interval (s)')
        refresh_interval_label.setFixedWidth(100)
        self.refresh_interval_edit = QLineEdit('10')
        lay_hor_interval.addWidget(refresh_interval_label)
        lay_hor_interval.addWidget(self.refresh_interval_edit)

        lay_hor_button = QHBoxLayout()
        self.btn_Scan = QPushButton("START")
        self.btn_Close = QPushButton("CLOSE")
        self.btn_Scan.clicked.connect(self.on_btn_StartOrStop_Clicked)
        self.btn_Close.clicked.connect(self.on_btn_Close_Clicked)
        lay_hor_button.addWidget(self.btn_Scan)
        lay_hor_button.addWidget(self.btn_Close)

        layout.addLayout(buyBotUI)
        layout.addLayout(sellBotUI)
        layout.addLayout(lay_hor_interval)
        layout.addLayout(lay_hor_button)

        self.statusBar().showMessage('Ready')
        centralWnd = QWidget()
        centralWnd.setLayout(layout)
        self.setCentralWidget(centralWnd)
        self.setFixedSize(500, 420)
        self.setWindowTitle("LOCALBITCOIN TRADING BOT")

    # Init buy bot ui part
    def initBuyBotUI(self):
        reg_ex = QRegExp("[0-9]*\.?[0-9]*")
        title_font = QFont()
        title_font.setPointSize(16)

        # Implememt GUI
        layout = QVBoxLayout()

        lay_hor_buy_1 = QHBoxLayout()
        buy_title_label = QLabel('Sell Bot')
        buy_title_label.setAlignment(Qt.AlignCenter)
        buy_title_label.setFont(title_font)
        lay_hor_buy_1.addWidget(buy_title_label)

        lay_hor_buy_2 = QHBoxLayout()
        buy_country_code_label = QLabel('Country Code')
        buy_country_code_label.setFixedWidth(100)
        self.buy_country_code_edit = QLineEdit('se')
        buy_country_name_label = QLabel('Country Name')
        buy_country_name_label.setFixedWidth(100)
        self.buy_country_name_edit = QLineEdit('sweden')
        lay_hor_buy_2.addWidget(buy_country_code_label)
        lay_hor_buy_2.addWidget(self.buy_country_code_edit)
        lay_hor_buy_2.addWidget(buy_country_name_label)
        lay_hor_buy_2.addWidget(self.buy_country_name_edit)

        lay_hor_buy_3 = QHBoxLayout()
        buy_payment_method_label = QLabel('Payment Method')
        buy_payment_method_label.setFixedWidth(100)
        self.buy_payment_method_edit = QLineEdit('swish')
        buy_higher_label = QLabel('Higher Value (USD)')
        buy_higher_label.setFixedWidth(100)
        self.buy_higher_edit = QLineEdit('1')
        buy_higher_validator = QRegExpValidator(reg_ex, self.buy_higher_edit)
        self.buy_higher_edit.setValidator(buy_higher_validator)
        lay_hor_buy_3.addWidget(buy_payment_method_label)
        lay_hor_buy_3.addWidget(self.buy_payment_method_edit)
        lay_hor_buy_3.addWidget(buy_higher_label)
        lay_hor_buy_3.addWidget(self.buy_higher_edit)

        lay_hor_buy_4 = QHBoxLayout()
        buy_lowest_label = QLabel('Lowest Value (USD)')
        buy_lowest_label.setFixedWidth(100)
        self.buy_lowest_edit = QLineEdit('7000')
        buy_lowest_validator = QRegExpValidator(reg_ex, self.buy_lowest_edit)
        self.buy_lowest_edit.setValidator(buy_lowest_validator)
        buy_highest_label = QLabel('Highest Value (USD)')
        buy_highest_label.setFixedWidth(100)
        self.buy_highest_edit = QLineEdit('8000')
        buy_highest_validator = QRegExpValidator(reg_ex, self.buy_highest_edit)
        self.buy_highest_edit.setValidator(buy_highest_validator)
        lay_hor_buy_4.addWidget(buy_lowest_label)
        lay_hor_buy_4.addWidget(self.buy_lowest_edit)
        lay_hor_buy_4.addWidget(buy_highest_label)
        lay_hor_buy_4.addWidget(self.buy_highest_edit)

        lay_hor_buy_5 = QHBoxLayout()
        buy_bot_key_label = QLabel('Buy-Bot Auth Key')
        buy_bot_key_label.setFixedWidth(100)
        self.buy_bot_key_edit = QLineEdit('c210d587696cc6bbcfd302be02ee6127')
        lay_hor_buy_5.addWidget(buy_bot_key_label)
        lay_hor_buy_5.addWidget(self.buy_bot_key_edit)

        lay_hor_buy_6 = QHBoxLayout()
        buy_bot_secret_label = QLabel('Buy-Bot Auth Secret')
        buy_bot_secret_label.setFixedWidth(100)
        self.buy_bot_secret_edit = QLineEdit('50c2267330b14f4f82832fb1836684cefc436063ec7db0c92c532ccf23a6fba0')
        lay_hor_buy_6.addWidget(buy_bot_secret_label)
        lay_hor_buy_6.addWidget(self.buy_bot_secret_edit)

        layout.addLayout(lay_hor_buy_1)
        layout.addLayout(lay_hor_buy_2)
        layout.addLayout(lay_hor_buy_3)
        layout.addLayout(lay_hor_buy_4)
        layout.addLayout(lay_hor_buy_5)
        layout.addLayout(lay_hor_buy_6)

        return layout

    # Init sell bot ui part
    def initSellBotUI(self):
        reg_ex = QRegExp("[0-9]*\.?[0-9]*")
        title_font = QFont()
        title_font.setPointSize(16)

        # Implememt GUI
        layout = QVBoxLayout()

        lay_hor_sell_1 = QHBoxLayout()
        sell_title_label = QLabel('Buy Bot')
        sell_title_label.setAlignment(Qt.AlignCenter)
        sell_title_label.setFont(title_font)
        lay_hor_sell_1.addWidget(sell_title_label)

        lay_hor_sell_2 = QHBoxLayout()
        sell_country_code_label = QLabel('Country Code')
        sell_country_code_label.setFixedWidth(100)
        self.sell_country_code_edit = QLineEdit('se')
        sell_country_name_label = QLabel('Country Name')
        sell_country_name_label.setFixedWidth(100)
        self.sell_country_name_edit = QLineEdit('sweden')
        lay_hor_sell_2.addWidget(sell_country_code_label)
        lay_hor_sell_2.addWidget(self.sell_country_code_edit)
        lay_hor_sell_2.addWidget(sell_country_name_label)
        lay_hor_sell_2.addWidget(self.sell_country_name_edit)

        lay_hor_sell_3 = QHBoxLayout()
        sell_payment_method_label = QLabel('Payment Method')
        sell_payment_method_label.setFixedWidth(100)
        self.sell_payment_method_edit = QLineEdit('swish')
        sell_lower_label = QLabel('Lower Value (USD)')
        sell_lower_label.setFixedWidth(100)
        self.sell_lower_edit = QLineEdit('1')
        sell_lower_validator = QRegExpValidator(reg_ex, self.sell_lower_edit)
        self.sell_lower_edit.setValidator(sell_lower_validator)
        lay_hor_sell_3.addWidget(sell_payment_method_label)
        lay_hor_sell_3.addWidget(self.sell_payment_method_edit)
        lay_hor_sell_3.addWidget(sell_lower_label)
        lay_hor_sell_3.addWidget(self.sell_lower_edit)

        lay_hor_sell_4 = QHBoxLayout()
        sell_lowest_label = QLabel('Lowest Value (USD)')
        sell_lowest_label.setFixedWidth(100)
        self.sell_lowest_edit = QLineEdit('7000')
        sell_lowest_validator = QRegExpValidator(reg_ex, self.sell_lowest_edit)
        self.sell_lowest_edit.setValidator(sell_lowest_validator)
        sell_highest_label = QLabel('Highest Value (USD)')
        sell_highest_label.setFixedWidth(100)
        self.sell_highest_edit = QLineEdit('8000')
        sell_highest_validator = QRegExpValidator(reg_ex, self.sell_highest_edit)
        self.sell_highest_edit.setValidator(sell_highest_validator)
        lay_hor_sell_4.addWidget(sell_lowest_label)
        lay_hor_sell_4.addWidget(self.sell_lowest_edit)
        lay_hor_sell_4.addWidget(sell_highest_label)
        lay_hor_sell_4.addWidget(self.sell_highest_edit)

        lay_hor_sell_5 = QHBoxLayout()
        sell_bot_key_label = QLabel('Sell-Bot Auth Key')
        sell_bot_key_label.setFixedWidth(100)
        self.sell_bot_key_edit = QLineEdit('1b33c78346dcb50e37a5c7f0672db14f')
        lay_hor_sell_5.addWidget(sell_bot_key_label)
        lay_hor_sell_5.addWidget(self.sell_bot_key_edit)

        lay_hor_sell_6 = QHBoxLayout()
        sell_bot_secret_label = QLabel('Sell-Bot Auth Secret')
        sell_bot_secret_label.setFixedWidth(100)
        self.sell_bot_secret_edit = QLineEdit('f1a2adcf3accce3d6bec25272320f8ac568991d4866ecfbd74f25d8c343760dc')
        lay_hor_sell_6.addWidget(sell_bot_secret_label)
        lay_hor_sell_6.addWidget(self.sell_bot_secret_edit)

        layout.addLayout(lay_hor_sell_1)
        layout.addLayout(lay_hor_sell_2)
        layout.addLayout(lay_hor_sell_3)
        layout.addLayout(lay_hor_sell_4)
        layout.addLayout(lay_hor_sell_5)
        layout.addLayout(lay_hor_sell_6)

        return layout

    # enable or disable controls according to the current status
    def enable_controls(self, flag = False):
        self.btn_Close.setEnabled(flag)
        self.refresh_interval_edit.setEnabled(flag)

        self.buy_higher_edit.setEnabled(flag)
        self.buy_lowest_edit.setEnabled(flag)
        self.buy_highest_edit.setEnabled(flag)
        self.buy_country_code_edit.setEnabled(flag)
        self.buy_country_name_edit.setEnabled(flag)
        self.buy_payment_method_edit.setEnabled(flag)
        self.buy_bot_key_edit.setEnabled(flag)
        self.buy_bot_secret_edit.setEnabled(flag)

        self.sell_lower_edit.setEnabled(flag)
        self.sell_lowest_edit.setEnabled(flag)
        self.sell_highest_edit.setEnabled(flag)
        self.sell_country_code_edit.setEnabled(flag)
        self.sell_country_name_edit.setEnabled(flag)
        self.sell_payment_method_edit.setEnabled(flag)
        self.sell_bot_key_edit.setEnabled(flag)
        self.sell_bot_secret_edit.setEnabled(flag)

    def on_btn_StartOrStop_Clicked(self):
        if (self.btn_Scan.text() == 'START'):
            buy_higher_value = self.buy_higher_edit.text()
            buy_lowest_value = self.buy_lowest_edit.text()
            buy_highest_value = self.buy_highest_edit.text()
            buy_country_code = self.buy_country_code_edit.text()
            buy_country_name = self.buy_country_name_edit.text()
            buy_payment_method = self.buy_payment_method_edit.text()
            buy_key = self.buy_bot_key_edit.text()
            buy_secret = self.buy_bot_secret_edit.text()

            sell_lower_value = self.sell_lower_edit.text()
            sell_lowest_value = self.sell_lowest_edit.text()
            sell_highest_value = self.sell_highest_edit.text()
            sell_country_code = self.sell_country_code_edit.text()
            sell_country_name = self.sell_country_name_edit.text()
            sell_payment_method = self.sell_payment_method_edit.text()
            sell_key = self.sell_bot_key_edit.text()
            sell_secret = self.sell_bot_secret_edit.text()

            refresh_interval = self.refresh_interval_edit.text()

            gbuyBot.start_thread(buy_higher_value, buy_lowest_value, buy_highest_value, buy_country_code, buy_country_name, buy_payment_method,
                                  buy_key, buy_secret, refresh_interval)
            gsellBot.start_thread(sell_lower_value, sell_lowest_value, sell_highest_value, sell_country_code, sell_country_name, sell_payment_method,
                                  sell_key, sell_secret, refresh_interval)

            self.statusBar().showMessage('Working.....')
            self.btn_Scan.setText('STOP')
            self.enable_controls(False)
        else:
            gbuyBot.stop_thread()
            gsellBot.stop_thread()
            self.statusBar().showMessage('Stopped.....')
            self.btn_Scan.setText('START')
            self.enable_controls(True)

    def on_btn_Close_Clicked(self):
        sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gbuyBot = LocalBitcoinBuyBot()
    gsellBot = LocalBitcoinSellBot()
    window = MainWnd()
    window.show()
    sys.exit(app.exec())
