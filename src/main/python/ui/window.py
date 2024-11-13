import sys
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from utils.encryption import md5
from domain.dao.pul_dao import PulDao
from utils.dt import get_day_offset

from env import Env


class MainForm(QWidget):
    env = Env()
    config = env.config
    tb_start_time = None
    tb_end_time = None
    tv_content = None
    btn_query = None

    def __init__(self, parent):
        super(MainForm, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        v_box = QVBoxLayout(self)
        v_box.addLayout(self.init_top_panel())
        v_box.addLayout(self.init_content_panel())

    def init_content_panel(self):
        box = QHBoxLayout()
        self.tv_content = QTableWidget(10, 9, self)
        headers = self.config.get('wnd', 'grid').split(',')
        columns = []
        for header in headers:
            columns.append(header.replace(' ', '\r\n'))
        self.tv_content.setHorizontalHeaderLabels(columns)
        header = self.tv_content.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        box.addWidget(self.tv_content, 10)
        return box

    def init_top_panel(self):
        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignLeft)

        lbl_start_time = QLabel(self)
        lbl_start_time.setText('StartTime')
        h_box.addWidget(lbl_start_time)

        start_time = get_day_offset(-1, True)
        end_time = datetime.now()

        self.tb_start_time = QDateTimeEdit(self)
        self.tb_start_time.setDateTime(start_time)
        h_box.addWidget(self.tb_start_time)

        lbl_end_time = QLabel(self)
        lbl_end_time.setText('EndTime')
        h_box.addWidget(lbl_end_time)

        self.tb_end_time = QDateTimeEdit(self)
        self.tb_end_time.setDateTime(end_time)
        h_box.addWidget(self.tb_end_time)

        self.btn_query = QPushButton(self)
        self.btn_query.setText("Query")
        self.btn_query.clicked.connect(self.btn_query_clicked)
        h_box.addWidget(self.btn_query)

        return h_box

    def btn_query_clicked(self):
        start_time = self.tb_start_time.text()
        end_time = self.tb_end_time.text()
        self.logger.debug("startTime: {0}, endTime: {1}".format(start_time, end_time))
        dao = PulDao(None, self.session, None)
        items = dao.get_pul_log(start_time, end_time)
        self.tv_content.setRowCount(len(items))

        column = 0
        for item in items:
            login_status = 'success' if item.log_in_status == 1 else 'failed'
            query_status = 'success' if item.query_status == 1 else 'failed'
            status = 'success' if item.status == 1 else 'failed'
            self.tv_content.setItem(column, 0, QTableWidgetItem(item.trans_time.strftime("%x %X")))
            self.tv_content.setItem(column, 1, QTableWidgetItem(login_status))
            self.tv_content.setItem(column, 2, QTableWidgetItem(query_status))
            self.tv_content.setItem(column, 3, QTableWidgetItem(str(item.total)))
            self.tv_content.setItem(column, 4, QTableWidgetItem(str(item.delivered)))
            self.tv_content.setItem(column, 5, QTableWidgetItem(str(item.revision_duplicated)))
            self.tv_content.setItem(column, 6, QTableWidgetItem(str(item.revision_changed)))
            self.tv_content.setItem(column, 7, QTableWidgetItem(str(item.fresh_item)))
            self.tv_content.setItem(column, 8, QTableWidgetItem(status))
            column += 1


class SystemTrayIcon(QSystemTrayIcon):
    mainWindow = None

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.mainWindow = parent
        self.config = parent.config
        menu = QMenu(parent)

        action_open_window = menu.addAction('Open window ...')
        menu.addSeparator()
        action_exist = menu.addAction('Exist Application ...')

        self.setContextMenu(menu)
        action_open_window.triggered.connect(self.mnu_show_main_window_clicked)
        action_exist.triggered.connect(self.mnu_exit_application_clicked)

    def mnu_show_main_window_clicked(self):
        self.hide()
        self.mainWindow.show()

    def mnu_exit_application_clicked(self):
        password = self.config.get('close', 'pwd')
        text, ok = QInputDialog.getText(None, "Attention", "Password?", QLineEdit.Password)
        if ok:
            text = md5(text)
            if text == password:
                self.hide()
                self.mainWindow.close()
                sys.exit(0)
        self.mnu_show_main_window_clicked()


class MainWindow(QMainWindow):
    env = Env()
    config = env.config
    context = env.context
    logger = env.logger

    closable = False
    lbl_status_bar = None
    tray_icon = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(300, 300, 960, 480)
        self.center()
        # application icon
        self.init_ui()

    def init_ui(self):
        # window title
        title = self.config.get('wnd', 'title')
        self.setWindowTitle(title)

        # window icon
        icon_image = self.config.get('wnd', 'icon')
        icon_file = self.context.get_resource(icon_image)
        # self.logger.debug(icon_file)
        icon = QIcon(icon_file)
        self.setWindowIcon(icon)

        # main form
        main_form = MainForm(self)
        self.setCentralWidget(main_form)

        # status bar
        self.statusBar().autoFillBackground()
        self.lbl_status_bar = QLabel(self)
        self.lbl_status_bar.setText("Hello")
        self.statusBar().addWidget(self.lbl_status_bar, 1)

        # tray icon
        self.tray_icon = SystemTrayIcon(icon, self)

    def update_status_bar_text(self, text):
        self.lbl_status_bar.setText(text)

    def closeEvent(self, event):
        self.hide()
        self.tray_icon.show()
        event.ignore()

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
