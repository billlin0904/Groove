# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from View.main_window import MainWindow

app = QApplication(sys.argv)

app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# 设置语言
translator = QTranslator()
translator.load(QLocale.system(), ":/i18n/Groove_")
app.installTranslator(translator)

# 创建主界面
groove = MainWindow()
groove.show()

sys.exit(app.exec_())