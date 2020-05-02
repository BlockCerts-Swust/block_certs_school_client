# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/4/28 15:33
@File      : main.py
@Version   : 1.0
@Description: 
"""
from threading import Thread

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QStyleFactory, QWidget,
                             QGridLayout, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog,
                             QSlider, QLabel, QLineEdit, QPushButton, QTableWidget, QGraphicsLayoutItem, QFrame,
                             QStackedLayout, QTextBrowser, QComboBox, QRadioButton, QVBoxLayout)
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import Qt, QTranslator, QEvent
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import pyqtgraph.exporters as pe
import qdarkstyle, requests, sys, time, random, json, datetime, re
import os
path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
father_path = os.path.abspath(path + os.path.sep +  "..")
sys.path.append(father_path)
from src.cert_issuer import config as cert_issue_config
from src.cert_issuer import issue_certificates
from src.main.api import school_login, get_cert, get_cert_detail, cert_issue
from src.main.utils import read_config_key, write_config_key


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))

class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置绘图背景
        pg.setConfigOption('background', '#19232D')
        pg.setConfigOption('foreground', 'd')
        pg.setConfigOptions(antialias=True)

        # 窗口居中显示
        self.center()
        self.resize(953, 592)
        self.init_ui()

        # 默认的状态栏
        # 可以设置其他按钮点击 参考多行文本显示 然而不行
        self.status = self.statusBar()
        # self.status.showMessage("我在主页面～")

        # 标题栏
        self.setWindowTitle(self.tr(u"Issue cert"))

    def init_ui(self):
        # self.setFixedSize(960,700)

        # 创建窗口主部件
        self.main_widget = QWidget()
        # 创建主部件的网格布局
        self.main_layout = QGridLayout()
        # 设置窗口主部件布局为网格布局
        self.main_widget.setLayout(self.main_layout)

        # 创建左侧部件
        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        # 创建左侧部件的网格布局层
        self.left_layout = QGridLayout()
        # 设置左侧部件布局为网格
        self.left_widget.setLayout(self.left_layout)

        # 创建右侧部件
        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        # 左侧部件上在第0行第0列，占12行5列
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 1)
        # 右侧部件在第0行第1列，占12行7列
        self.main_layout.addWidget(self.right_widget, 0, 1, 12, 7)
        # 设置窗口主部件
        self.setCentralWidget(self.main_widget)

        # function button
        self.cert_issue = QPushButton(self.tr(u"Issue cert"))
        self.left_layout.addWidget(self.cert_issue, 1, 0, 1, 5)

        self.quit_btn = QPushButton(self.tr(u"Log out"))
        self.quit_btn.clicked.connect(self.quit_act)
        self.left_layout.addWidget(self.quit_btn, 2, 0, 1, 5)

        # tablewidgt to view data
        self.query_result = QTableWidget()
        self.left_layout.addWidget(self.query_result, 9, 0, 2, 5)
        self.query_result.verticalHeader().setVisible(False)

        self.label1 = QLabel(self.tr(u"cert ID"))
        self.right_layout.addWidget(self.label1, 0, 1, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.cert_id = QLineEdit()
        self.cert_id.setPlaceholderText(self.tr(u"Please enter the cert ID you want to issue:"))
        self.right_layout.addWidget(self.cert_id, 0, 2, 1, 6)

        self.label = QLabel(self.tr(u"password"))
        self.right_layout.addWidget(self.label, 1, 1, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText(self.tr(u"please enter your password: "))
        self.right_layout.addWidget(self.password, 1, 2, 1, 6)

        self.label2 = QLabel(self.tr(u"Blockchain"))
        self.right_layout.addWidget(self.label2, 2, 1, 1, 1)
        self.cb = QComboBox()
        self.cb.addItems(['bitcoin_testnet', 'ethereum_ropsten', 'bitcoin_mainnet', 'ethereum_mainnet'])
        self.right_layout.addWidget(self.cb, 2, 2, 1, 5)

        self.issuer_button = QPushButton(self.tr(u"Issue"))
        self.issuer_button.clicked.connect(self.issue_cert)
        self.right_layout.addWidget(self.issuer_button, 2, 7, 1, 1)

        self.text_browser = QTextBrowser()
        self.right_layout.addWidget(self.text_browser, 3, 1, 5, 7)
        self.text_browser.setReadOnly(True)

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.main_layout.setSpacing(0)
        # 美化风格
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def quit_act(self):
        reply = QMessageBox.question(self, self.tr(u"info"),
                                    self.tr(u"Are you sure to exit?"),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            qApp = QApplication.instance()
            qApp.quit()
        else:
            return

    def issue_cert(self):
        rst = self.form_valid()
        if rst is False:
            QMessageBox.information(self, self.tr('information'), self.tr(u'Please fill in the issue information'))
            return
        if self.password.text() != read_config_key("USER", "password"):
            QMessageBox.information(self, self.tr('information'), self.tr(u'Password wrong'))
            return
        t = Thread(target=self.issue_function)
        t.start()

    def issue_function(self):
        try:
            cert_id = self.cert_id.text()
            api_token = read_config_key("USER", "api_token")
            issuing_address = read_config_key("USER", "public_key")
            secret_key = read_config_key("USER", "secret_key")
            chain = self.cb.currentText()
            self.text_Browser_add(cert_id + self.tr(" Issuing ... "))
            self.text_Browser_add(self.tr("\tGet cert info ..."))
            response = get_cert(cert_id, api_token)
            QApplication.processEvents()
            self.text_Browser_add(self.tr("\tGet cert detail ..."))
            cert_info = get_cert_detail(cert_id, api_token)
            QApplication.processEvents()
            self.text_Browser_add(self.tr("\tSigning and issuing cert, it will take a long time, please wait ..."))
            parsed_config = self.parsed_config(issuing_address, secret_key, cert_info, chain)
            QApplication.processEvents()
            tx_id, certificates_to_issue = issue_certificates.main(parsed_config)
            self.text_Browser_add(self.tr("\tblock_cert tx_id ") + tx_id)
            if tx_id:
                for _, metadata in certificates_to_issue.items():
                    block_cert = metadata.blockcert
                    self.text_Browser_add(self.tr("\tblock_cert upload..."))
                    cert_issue(cert_id=cert_id, api_token=api_token, block_cert=block_cert, tx_id=tx_id)
                    QApplication.processEvents()
                    break
                self.text_Browser_add("\t" + cert_id + self.tr("Issue success"))
            else:
                self.text_Browser_add(cert_id + self.tr(" Issue Fail"))
        except Exception as e:
            self.text_Browser_add(self.tr(" Issue Fail"))

    def form_valid(self):
        print(self.cert_id.text())
        if self.cert_id.text() is "":
            return False
        print(self.password.text())
        if self.password.text() is "":
            return False
        print(self.cb.currentText())
        if self.cb.currentText() is "":
            return False
        return True

    def parsed_config(self, issuing_address, secret_key, cert_info, chain):
        base_config = {
            "api_token": None,
            "batch_size": 10,
            "bitcoind": False,
            "blockcypher_api_token": None,
            "chain": chain,
            "dust_threshold": 0.0000275,
            "gas_limit": 25000,
            "gas_price": 20000000000,
            "issuing_address": issuing_address,
            "secret_key": secret_key,
            "max_retry": 10,
            "my_config": None,
            "safe_mode": False,
            "satoshi_per_byte": 250,
            "tx_fee": 0.0006,
            "unsigned_certificates":{cert_info["unsign_cert"]["id"]: cert_info["unsign_cert"]}
        }
        config = cert_issue_config.get_config(base_config)
        return config

    def text_Browser_add(self, message):
        print(message)
        self.text_browser.append(message)
        self.cursor = self.text_browser.textCursor()
        self.text_browser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()


class LoginUi(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置绘图背景
        pg.setConfigOption('background', '#19232D')
        pg.setConfigOption('foreground', 'd')
        pg.setConfigOptions(antialias=True)

        # 窗口居中显示
        self.center()

        self.resize(438, 300)

        self.init_ui()

        # 默认的状态栏
        # 可以设置其他按钮点击 参考多行文本显示 然而不行
        self.status = self.statusBar()
        # self.status.showMessage("我在主页面～")

        # 标题栏
        self.setWindowTitle(self.tr(u"Login"))
        language = read_config_key("USER", "language")
        if language == "zh_CN":
            self.trans.load('zh_CN')
            _app = QApplication.instance()
            _app.installTranslator(self.trans)

    def init_ui(self):
        # self.setFixedSize(960,700)

        # 创建窗口主部件
        self.main_widget = QWidget()
        # 创建主部件的网格布局
        self.main_layout = QGridLayout()
        # 设置窗口主部件布局为网格布局
        self.main_widget.setLayout(self.main_layout)

        # 设置窗口主部件
        self.setCentralWidget(self.main_widget)

        self.combo = QComboBox(self)
        if read_config_key("USER", "language") == "zh_CN":
            self.combo.addItems(['中文', 'English'])
        else:
            self.combo.addItems(['English', '中文'])
        self.combo.currentTextChanged.connect(self.change_func)

        self.trans = QTranslator(self)

        self.main_layout.addWidget(self.combo, 0, 0, 1, 3)

        self.username_label = QLabel(self.tr(u"username"))
        self.main_layout.addWidget(self.username_label, 1, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.username = QLineEdit()
        self.username.setPlaceholderText(self.tr(u"Please enter your username:"))
        self.main_layout.addWidget(self.username, 1, 1, 1, 11)

        self.password_label = QLabel(self.tr(u"password"))
        self.main_layout.addWidget(self.password_label, 2, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText(self.tr(u"Please enter your password:"))
        self.main_layout.addWidget(self.password, 2, 1, 1, 11)

        self.private_key_label = QLabel(self.tr(u"Private key"))
        self.main_layout.addWidget(self.private_key_label, 3, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.private_key = QLineEdit()
        self.private_key.setEchoMode(QLineEdit.Password)
        self.private_key.setPlaceholderText(self.tr(u"Please enter your private key:"))
        self.main_layout.addWidget(self.private_key, 3, 1, 1, 11)

        self.remember_me_button = QRadioButton()
        self.main_layout.addWidget(self.remember_me_button, 4, 1, 1, 1)
        self.remember_me_label = QLabel(self.tr(u"remember me"))
        self.main_layout.addWidget(self.remember_me_label, 4, 2, 1, 4)

        self.login_button = QPushButton(self.tr(u"Login"), self)
        self.main_layout.addWidget(self.login_button, 4, 6, 1, 6)
        self.login_button.clicked.connect(self.login)

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.main_layout.setSpacing(0)
        # 美化风格
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.username.setText(read_config_key("USER", "username"))
        self.password.setText(read_config_key("USER", "password"))
        self.private_key.setText(read_config_key("USER", "secret_key"))

    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # language change
    def change_func(self):
        print(self.combo.currentText())
        if self.combo.currentText() == '中文':
            write_config_key("USER", "language", "zh_CN")
            self.trans.load('zh_CN')
            _app = QApplication.instance()
            _app.installTranslator(self.trans)

        else:
            write_config_key("USER", "language", "")
            _app = QApplication.instance()
            _app.removeTranslator(self.trans)

    # 更新UI
    def retranslateUi(self):        # 1
        self.username_label.setText(QApplication.translate('LoginUi', 'username'))
        self.username.setPlaceholderText(QApplication.translate('LoginUi','Please enter your username:'))
        self.password_label.setText(QApplication.translate('LoginUi', 'password'))
        self.password.setPlaceholderText(QApplication.translate('LoginUi', 'password'))
        self.private_key_label.setText(QApplication.translate('LoginUi', 'Private key'))
        self.private_key.setPlaceholderText(QApplication.translate('LoginUi', 'Please enter your private key:'))
        self.login_button.setText(QApplication.translate('LoginUi', 'Login'))
        self.remember_me_label.setText(QApplication.translate('LoginUi', 'remember me'))

    # 语言改变之后更新UI
    def changeEvent(self, event):   # 2
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()

    def login(self):
        rst = self.form_valid()
        if rst is False:
            QMessageBox.information(self, self.tr('information'), self.tr(u'Please fill in the login information'))
            return
        try:
            self.status.showMessage(self.tr("Login..."))
            QtWidgets.QApplication.processEvents()
            if self.remember_me_button.isChecked():
                write_config_key("USER", "username", self.username.text)
                write_config_key("USER", "password", self.password.text)
                write_config_key("USER", "secret_key", self.private_key.text)
            username = self.username.text()
            password = self.password.text()
            response = school_login(username, password)
            QApplication.processEvents()
            public_key = response["data"]["school"]["public_key"]
            api_token = response["data"]["token"]
            write_config_key("USER", "api_token", api_token)
            write_config_key("USER", "public_key", public_key)
            self.close()
            self.main = MainUi()
            self.main.show()
        except Exception as e:
            print(e)
            QMessageBox.information(self, self.tr('information'), self.tr(u'Login Fail'))
            return

    def form_valid(self):
        if self.username.text() is "":
            return False
        if self.password.text() is "":
            return False
        if self.private_key.text() is "":
            return False
        return True

def main():
    app = QApplication(sys.argv)
    gui = LoginUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # sys.path.append('D:/My Files/CodingZone/blockCertsClonedRepoSchoolClient/block_certs_school_client/src/main/main.py')
    main()