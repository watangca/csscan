from qt_core import *
from login.auth_module import *
from login.profilemanager import ProfileManager 
from login.usermanager import *
from gui.widgets import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes


class Page7Widget(QWidget):
    def __init__(self, username: str):
        super().__init__()

        # 설정 및 테마 로드
        settings = Settings()
        self.settings = settings.items
        themes = Themes()
        self.themes = themes.items

        user_manager = UserManager.get_instance()
        current_username = user_manager.get_current_user() if username is None else username
        self.username = current_username

        self.profile_manager = ProfileManager()

        self.current_user = {'username': username, 'email': ''}
        
        # Initialize user_label and email_label attributes
        self.user_label = None
        self.email_label = None
        
        self.setup_ui()
        self.load_profile()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # 저장 버튼과 스페이서를 포함하는 수평 레이아웃
        button_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        # 저장 버튼
        self.save_button = PyPushButton("저장")
        self.save_button.clicked.connect(self.save_profile)
        button_layout.addWidget(self.save_button)
        self.layout.addLayout(button_layout)

        # 테이블 위젯 설정
        self.table_widget = PyTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["프로필 구분", "상세 내용"])
        self.table_widget.setRowCount(7)

        # Stretch the last column of the header to fill the table
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 테이블 행 설정
        self.setup_table_rows()

        # 테이블 위젯을 메인 레이아웃에 추가
        self.layout.addWidget(self.table_widget)

    def setup_table_rows(self):
        labels = ["Profile User", "User Email", "first name", "last name", 
                "Company name", "Company web site", "Phone", "Country"]
        for i, label in enumerate(labels):
            label_item = QTableWidgetItem(label)
            label_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(i, 0, label_item)

            if label == "Profile User":
                self.user_label = QLabel(self.current_user['username'])
                self.user_label.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(i, 1, self.user_label)
            elif label == "User Email":
                self.email_label = QLabel()
                self.email_label.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(i, 1, self.email_label)
            else:
                line_edit = PyLineEdit()
                line_edit.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(i, 1, line_edit)

                # "Company web site" 라벨에 대한 특별 처리
                if label == "Company web site":
                    setattr(self, "company_web_site_entry", line_edit)
                else:
                    setattr(self, label.lower().replace(" ", "_") + "_entry", line_edit)

    def load_profile(self):
        try:
            # users 테이블에서 username과 email을 로딩합니다.
            user_info = self.profile_manager.get_user_info(self.username)
            if user_info:
                username, email = user_info
                self.user_label.setText(username)
                self.email_label.setText(email)
            else:
                self.user_label.setText("정보 없음")
                self.email_label.setText("정보 없음")

            # user_profiles 테이블에서 나머지 프로필 정보를 로딩합니다.
            profile_info = self.profile_manager.get_profile(self.current_user['username'])
            if profile_info:
                first_name, last_name, company_name, company_website, phone, country = profile_info
                self.first_name_entry.setText(first_name)
                self.last_name_entry.setText(last_name)
                self.company_name_entry.setText(company_name)
                self.company_web_site_entry.setText(company_website)  
                self.phone_entry.setText(phone)
                self.country_entry.setText(country)
        except Exception as e:
            print(f"프로필 로딩 중 오류 발생: {e}")
            QMessageBox.critical(self, "오류", "프로필을 로드하는 중 오류가 발생했습니다.")

    def save_profile(self):
        updated_info = {
            "first_name": self.first_name_entry.text(),
            "last_name": self.last_name_entry.text(),
            "company_name": self.company_name_entry.text(),
            "company_website": self.company_web_site_entry.text(),
            "phone": self.phone_entry.text(),
            "country": self.country_entry.text()
        }

        try:
            self.profile_manager.save_profile(self.current_user['username'], **updated_info)
            PyDialog.information(self, "저장 완료", "프로필 정보가 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"프로필 저장 중 오류 발생: {e}")
            PyDialog.warning(self, "오류", "프로필 정보를 저장하는 중 오류가 발생했습니다.")
