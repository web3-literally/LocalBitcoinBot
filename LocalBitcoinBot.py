
from PyQt5.QtWidgets import *
import sys
from LocalBitcoinBuyBot import LocalBitcoinBuyBot

# Scanning thread
gbuyAdsObserver = None

# Main window to show setting page
class MainWnd(QMainWindow):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)

        # Implememt GUI
        layout = QVBoxLayout()

        lay_hor_1 = QHBoxLayout()
        lower_label = QLabel('Lower  Value (USD)')
        self.lower_edit = QLineEdit('1')
        lay_hor_1.addWidget(lower_label)
        lay_hor_1.addWidget(self.lower_edit)

        lay_hor_2 = QHBoxLayout()
        lowest_label = QLabel('Lowest Value (USD)')
        self.lowest_edit = QLineEdit('7000')
        lay_hor_2.addWidget(lowest_label)
        lay_hor_2.addWidget(self.lowest_edit)

        lay_hor_3 = QHBoxLayout()
        highest_label = QLabel('Highest Value (USD)')
        self.highest_edit = QLineEdit('8000')
        lay_hor_3.addWidget(highest_label)
        lay_hor_3.addWidget(self.highest_edit)

        lay_hor_4 = QHBoxLayout()
        country_code_label = QLabel('Country Code')
        self.country_code_edit = QLineEdit('se')

        lay_hor_4.addWidget(country_code_label)
        lay_hor_4.addWidget(self.country_code_edit)

        lay_hor_5 = QHBoxLayout()
        country_name_label = QLabel('Country Name')
        self.country_name_edit = QLineEdit('sweden')

        lay_hor_5.addWidget(country_name_label)
        lay_hor_5.addWidget(self.country_name_edit)

        lay_hor_6 = QHBoxLayout()
        payment_method_label = QLabel('Payment Method')
        self.payment_method_edit = QLineEdit('swish')

        lay_hor_6.addWidget(payment_method_label)
        lay_hor_6.addWidget(self.payment_method_edit)

        lay_hor_7 = QHBoxLayout()
        auth_key_label = QLabel('Auth Key')
        self.auth_key_edit = QLineEdit('1b33c78346dcb50e37a5c7f0672db14f')

        lay_hor_7.addWidget(auth_key_label)
        lay_hor_7.addWidget(self.auth_key_edit)

        lay_hor_8 = QHBoxLayout()
        auth_secret_label = QLabel('Auth Secret')
        self.auth_secret_edit = QLineEdit('f1a2adcf3accce3d6bec25272320f8ac568991d4866ecfbd74f25d8c343760dc')

        lay_hor_8.addWidget(auth_secret_label)
        lay_hor_8.addWidget(self.auth_secret_edit)

        lay_hor_9 = QHBoxLayout()
        refresh_interval_label = QLabel('Refresh Interval (s)')
        self.refresh_interval_edit = QLineEdit('10')

        lay_hor_9.addWidget(refresh_interval_label)
        lay_hor_9.addWidget(self.refresh_interval_edit)

        lay_hor_10 = QHBoxLayout()
        self.btn_Scan = QPushButton("START")
        self.btn_Close = QPushButton("CLOSE")
        self.btn_Scan.clicked.connect(self.on_btn_StartOrStop_Clicked)
        self.btn_Close.clicked.connect(self.on_btn_Close_Clicked)
        lay_hor_10.addWidget(self.btn_Scan)
        lay_hor_10.addWidget(self.btn_Close)

        layout.addLayout(lay_hor_1)
        layout.addLayout(lay_hor_2)
        layout.addLayout(lay_hor_3)
        layout.addLayout(lay_hor_4)
        layout.addLayout(lay_hor_5)
        layout.addLayout(lay_hor_6)
        layout.addLayout(lay_hor_7)
        layout.addLayout(lay_hor_8)
        layout.addLayout(lay_hor_9)
        layout.addLayout(lay_hor_10)

        self.statusBar().showMessage('Ready')
        centralWnd = QWidget()
        centralWnd.setLayout(layout)
        self.setCentralWidget(centralWnd)
        self.setFixedSize(500, 350)
        self.setWindowTitle("LOCALBITCOIN TRADING BOT")

    # enable or disable controls according to the current status
    def enable_controls(self, flag = False):
        self.btn_Close.setEnabled(flag)
        self.lower_edit.setEnabled(flag)
        self.lowest_edit.setEnabled(flag)
        self.highest_edit.setEnabled(flag)
        self.country_code_edit.setEnabled(flag)
        self.country_name_edit.setEnabled(flag)
        self.payment_method_edit.setEnabled(flag)
        self.auth_key_edit.setEnabled(flag)
        self.auth_secret_edit.setEnabled(flag)
        self.refresh_interval_edit.setEnabled(flag)

    def on_btn_StartOrStop_Clicked(self):
        if (self.btn_Scan.text() == 'START'):
            lower_value = self.lower_edit.text()
            lowest_value = self.lowest_edit.text()
            highest_value = self.highest_edit.text()
            country_code = self.country_code_edit.text()
            country_name = self.country_name_edit.text()
            payment_method = self.payment_method_edit.text()
            auth_key = self.auth_key_edit.text()
            auth_secret = self.auth_secret_edit.text()
            refresh_interval = self.refresh_interval_edit.text()
            gbuyAdsObserver.start_thread(lower_value, lowest_value, highest_value, country_code, country_name, payment_method, auth_key, auth_secret, refresh_interval)
            self.statusBar().showMessage('Working.....')
            self.btn_Scan.setText('STOP')
            self.enable_controls(False)
        else:
            gbuyAdsObserver.stop_thread()
            self.statusBar().showMessage('Stopped.....')
            self.btn_Scan.setText('START')
            self.enable_controls(True)

    def on_btn_Close_Clicked(self):
        sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gbuyAdsObserver = LocalBitcoinBuyBot()
    window = MainWnd()
    window.show()
    sys.exit(app.exec())
