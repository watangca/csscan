from qt_core import *
from login.sessionmanager import *
from login.usermanager import *
from gui.uis.pages.page_1 import Page1Widget
from gui.uis.pages.page_2.page_2_linux import Page2LinuxWidget
from gui.uis.pages.page_2.page_2_windows import Page2WindowsWidget
from gui.uis.pages.page_2.page_2_database import Page2DatabaseWidget
from gui.uis.pages.page_3.page_3_linux import Page3LinuxWidget
from gui.uis.pages.page_3.page_3_windows import Page3WindowsWidget
from gui.uis.pages.page_3.page_3_database import Page3DatabaseWidget
from gui.uis.pages.page_4.page_4_excel import Page4ExcelWidget
# from gui.uis.pages.page_4.page_4_word import Page4WordWidget
from gui.uis.pages.page_5.page_5_linux import Page5LinuxWidget
from gui.uis.pages.page_5.page_5_windows import Page5WindowsWidget
from gui.uis.pages.page_5.page_5_database import Page5DatabaseWidget
from gui.uis.pages.page_6.page_6_management import Page6ManagementWidget
from gui.uis.pages.page_6.page_6_history import Page6HistoryWidget
from gui.uis.pages.page_7 import Page7Widget
from gui.uis.pages.page_8 import Page8Widget 


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
  
        # Adding custom page widgets to the QStackedWidget
        self.page_1_widget = Page1Widget()
        self.pages.addWidget(self.page_1_widget)

        self.page_2_linux_widget = Page2LinuxWidget()
        self.pages.addWidget(self.page_2_linux_widget)        

        self.page_2_windows_widget = Page2WindowsWidget()
        self.pages.addWidget(self.page_2_windows_widget)

        self.page_2_database_widget = Page2DatabaseWidget()
        self.pages.addWidget(self.page_2_database_widget)

        self.page_3_linux_widget = Page3LinuxWidget()
        self.pages.addWidget(self.page_3_linux_widget)
        self.page_2_linux_widget.dataChanged.connect(self.page_3_linux_widget.load_linux_data)

        self.page_3_windows_widget = Page3WindowsWidget()
        self.pages.addWidget(self.page_3_windows_widget)
        self.page_2_windows_widget.dataChanged.connect(self.page_3_windows_widget.load_windows_data)

        self.page_3_database_widget = Page3DatabaseWidget()
        self.pages.addWidget(self.page_3_database_widget)
        self.page_2_database_widget.dataChanged.connect(self.page_3_database_widget.load_database_data)

        self.page_4_excel_widget = Page4ExcelWidget()
        self.pages.addWidget(self.page_4_excel_widget)

        # self.page_4_word_widget = Page4WordWidget()
        # self.pages.addWidget(self.page_4_word_widget)

        self.page_5_linux_widget = Page5LinuxWidget()
        self.pages.addWidget(self.page_5_linux_widget)

        self.page_5_windows_widget = Page5WindowsWidget()
        self.pages.addWidget(self.page_5_windows_widget)

        self.page_5_database_widget = Page5DatabaseWidget()
        self.pages.addWidget(self.page_5_database_widget)

        self.page_6_management_widget = Page6ManagementWidget()
        self.pages.addWidget(self.page_6_management_widget)

        self.page_6_history_widget = Page6HistoryWidget()
        self.pages.addWidget(self.page_6_history_widget)

        current_user = UserManager.get_instance().get_current_user()
        self.page_7_widget = Page7Widget(current_user)
        self.pages.addWidget(self.page_7_widget)

        self.page_8_widget = Page8Widget()
        self.pages.addWidget(self.page_8_widget)

        self.main_pages_layout.addWidget(self.pages)

        self.retranslateUi(MainPages)
        self.pages.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainPages)

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"MainPages", None))
