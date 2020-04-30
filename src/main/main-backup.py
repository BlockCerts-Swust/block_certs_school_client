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
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QStyleFactory, QWidget,
                             QGridLayout, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog,
                             QSlider, QLabel, QLineEdit, QPushButton, QTableWidget, QGraphicsLayoutItem, QFrame,
                             QStackedLayout, QTextBrowser, QComboBox, QRadioButton)
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import Qt
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import pyqtgraph.exporters as pe
import qdarkstyle, requests, sys, time, random, json, datetime, re

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
        self.setWindowTitle("证书颁发")

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
        self.cert_issue = QPushButton("证书颁发")
        self.left_layout.addWidget(self.cert_issue, 1, 0, 1, 5)

        self.quit_btn = QPushButton("退出")
        self.quit_btn.clicked.connect(self.quit_act)
        self.left_layout.addWidget(self.quit_btn, 2, 0, 1, 5)

        # tablewidgt to view data
        self.query_result = QTableWidget()
        self.left_layout.addWidget(self.query_result, 9, 0, 2, 5)
        self.query_result.verticalHeader().setVisible(False)

        self.label1 = QLabel("证书ID")
        self.right_layout.addWidget(self.label1, 0, 1, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.cert_id = QLineEdit()
        self.cert_id.setPlaceholderText("请输入您想颁发的证书ID：")
        self.right_layout.addWidget(self.cert_id, 0, 2, 1, 6)

        self.label = QLabel("密码")
        self.right_layout.addWidget(self.label, 1, 1, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("请输入您的密码：")
        self.right_layout.addWidget(self.password, 1, 2, 1, 6)

        self.label2 = QLabel("区块链")
        self.right_layout.addWidget(self.label2, 2, 1, 1, 1)
        self.cb = QComboBox()
        self.cb.addItems(['bitcoin_testnet', 'ethereum_ropsten', 'bitcoin_mainnet', 'ethereum_mainnet'])
        self.right_layout.addWidget(self.cb, 2, 2, 1, 5)

        self.issuer_button = QPushButton("颁发")
        self.right_layout.addWidget(self.issuer_button, 2, 7, 1, 1)

        self.plot_console = QTextBrowser()
        self.right_layout.addWidget(self.plot_console, 3, 1, 5, 7)

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
        self.setWindowTitle("登录")

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

        self.label = QLabel("账号")
        self.main_layout.addWidget(self.label, 0, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.cert_id = QLineEdit()
        self.cert_id.setPlaceholderText("请输入您的账号：")
        self.main_layout.addWidget(self.cert_id, 0, 1, 1, 11)

        self.label = QLabel("密码")
        self.main_layout.addWidget(self.label, 1, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("请输入您的密码：")
        self.main_layout.addWidget(self.password, 1, 1, 1, 11)

        self.label = QLabel("私钥")
        self.main_layout.addWidget(self.label, 2, 0, 1, 1)
        # 右侧部件在第1行第1列，占1行6列
        self.private_key = QLineEdit()
        self.private_key.setEchoMode(QLineEdit.Password)
        self.private_key.setPlaceholderText("请输入您的私钥：")
        self.main_layout.addWidget(self.private_key, 2, 1, 1, 11)

        self.remember_me_button = QRadioButton()
        self.main_layout.addWidget(self.remember_me_button, 3, 1, 1, 1)
        self.label = QLabel("记住我")
        self.main_layout.addWidget(self.label, 3, 2, 1, 4)

        self.issuer_button = QPushButton("登录")
        self.main_layout.addWidget(self.issuer_button, 3, 6, 1, 6)
        self.issuer_button.clicked.connect(self.login)

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


def main():
    app = QApplication(sys.argv)
    gui = LoginUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()