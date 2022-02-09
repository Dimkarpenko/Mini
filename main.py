from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import os
import sys

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        
        QBtn = QDialogButtonBox.Ok
        self.buttonbox = QDialogButtonBox(QBtn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.rejected)

        layout = QVBoxLayout()

        title = QLabel("Mini Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'icon.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 0.2"))
        layout.addWidget(QLabel("Copyright 2021 Dmitry Karpenko"))

        pylogo = QLabel()
        pylogo.setPixmap(QPixmap(os.path.join('images', 'python-powered.png')))
        layout.addWidget(pylogo)

        self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))
        self.resize(400,200)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonbox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    htmlFinished = pyqtSignal()
    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        
        self.mHtml = ""
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.shortcut.activated.connect(self.add_new_tab)

        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.open_file)

        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.save_file)

        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.close_current_tab)

        self.shortcut = QShortcut(QKeySequence("Ctrl+f5"), self)
        self.shortcut.activated.connect(lambda: self.tabs.currentWidget().reload())

        self.shortcut = QShortcut(QKeySequence("Ctrl+LEFT"), self)
        self.shortcut.activated.connect(lambda: self.tabs.currentWidget().back())

        self.shortcut = QShortcut(QKeySequence("Ctrl+RIGHT"), self)
        self.shortcut.activated.connect(lambda: self.tabs.currentWidget().forward())

        self.shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        self.shortcut.activated.connect(self.navigate_home)

        self.shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut.activated.connect(self.view_source)

        #self.status = QStatusBar()
        #self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(30,30))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images','back-icon.png')),"Back (Ctrl+LEFT)",self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images','forward-icon.png')),"Forward (Ctrl+RIGHT)",self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images','reload-icon.png')),"Reload (Ctrl+f5)",self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images','home-icon.png')),"Home (Ctrl+B)",self)
        home_btn.setStatusTip("Go to Homepage")
        home_btn.triggered.connect(lambda: self.navigate_home())
        navtb.addAction(home_btn)

        navtb.addSeparator()
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', '')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images','stop-icon.png')),"Stop",self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)       

        file_menu = self.menuBar().addMenu('&File')

        new_tab_action = QAction(QIcon(os.path.join('images','newtab-icon.png')),"New Tab     (Ctrl+N)",self)
        new_tab_action.setStatusTip("Open New Tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images','openfile-icon.png')),"Open file    (Ctrl+O)",self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
    
        save_file_action = QAction(QIcon(os.path.join('images','save-icon.png')),"Save page  (Ctrl+S)",self)
        save_file_action.setStatusTip("Open from file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        #просмотр истории не работает.Нужно добавить в функции view_history.Там сейчас просто pass
        view_history_action = QAction(QIcon(os.path.join('images','history-icon.png')),"Search history",self)
        view_history_action.setStatusTip("View search history")
        view_history_action.triggered.connect(self.view_history)
        #file_menu.addAction(view_history_action)

        tool_menu = self.menuBar().addMenu('&Tools')

        view_source_action = QAction(QIcon(os.path.join('images','viewcode-icon.png')),"View page code (Ctrl+W)",self)
        view_source_action.setStatusTip("View page source code")
        view_source_action.triggered.connect(self.view_source)
        tool_menu.addAction(view_source_action)

        help_menu = self.menuBar().addMenu('&Help')

        about_action = QAction(QIcon(os.path.join('images','about-icon.png')),"About browser",self)
        about_action.setStatusTip("Search")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        self.add_new_tab(QUrl("https://www.google.com/"), "Homepage")

        self.show()

        self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

    @pyqtSlot()
    def view_source(self):
        a = "view-source:"+self.urlbar.text()
        self.add_new_tab()
        self.tabs.currentWidget().setUrl(QUrl(a))

    def view_history(self):
        pass

    def add_new_tab(self, qurl=None, label="New tab"):

        if qurl is None:
            qurl = QUrl('https://www.google.com/')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                    self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                    self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Mini" % title)

    def about(self):
        dig = AboutDialog()
        dig.exec_()

    def open_error(self):
        buttonReply = QMessageBox.question(self, 'Mini browser', "Используется неподдерживаемый тип файла!", QMessageBox.Ok)

    def save_error(self):
        buttonReply = QMessageBox.question(self, 'Mini browser', "Невозможно сохранить страницу, так как используется неподдерживаемый тип файла!", QMessageBox.Ok)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Hypertext Markup Language (*.htm *.html);;" "All files(*.*)")
        if filename:
            with open(filename, 'r') as f:
                try:
                    html = f.read()
                    self.add_new_tab()
                    self.tabs.currentWidget().setHtml(html)
                    self.urlbar.setText(filename)
                except:
                    self.open_error()

    def callback(self, html):
        self.mHtml = html
        self.htmlFinished.emit()

    def save_file(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "Hypertext Markup Language (*.html);;" "All files(*.*)")
            if filename:
                self.tabs.currentWidget().page().toHtml(self.callback)
                loop = QEventLoop()
                self.htmlFinished.connect(loop.quit)
                loop.exec_()
                with open(filename, 'w') as f:
                    f.write(self.mHtml)
        except:
            self.save_error()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com/"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == "https":
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'https-icon.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'nohttps-icon.png')))
        
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass

app = QApplication(sys.argv)
app.setApplicationName("Mini browser")
app.setOrganizationName("Mini")
app.setOrganizationDomain("google.com")

window = MainWindow()
app.exec_()