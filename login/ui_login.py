import sys
import os
import socket
from qt_core import *
from main import MainWindow
from gui.widgets import *
from gui.core.functions import Functions 
from login.auth_module import *
from login.sessionmanager import *
from login.usermanager import *
from login.forgot_passwd import PasswordResetModule
from login.database.UserDatabaseManager import get_user_db_connection

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

class Ui_LoginWindow:
    def setupUi(self, MainWindow):
        self.login_window = MainWindow
        MainWindow.setWindowTitle('CSScan Login')
        MainWindow.setMinimumSize(350, 450)
        MainWindow.setMaximumSize(350, 450)

        # 기본 타이틀 바 숨기기
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        
        centralwidget = QWidget(MainWindow)
        centralwidget.setStyleSheet('background-color: #21252d;') 
        MainWindow.setCentralWidget(centralwidget)
        
        mainLayout = QVBoxLayout(centralwidget)

        # 커스텀 타이틀 바 생성 및 추가
        self.customTitleBar = CustomTitleBar(MainWindow)
        mainLayout.addWidget(self.customTitleBar)

        # 아이콘 프레임
        iconFrame = self.createIconFrame(MainWindow)
        mainLayout.addWidget(iconFrame)

        # 로그인 라벨 프레임
        signInLabelFrame = self.createSignInLabelFrame(MainWindow)
        mainLayout.addWidget(signInLabelFrame)

        # 입력 프레임
        inputFrame = self.createInputFrame(MainWindow)
        mainLayout.addWidget(inputFrame)

        # 액션 프레임
        actionFrame = self.createActionFrame(MainWindow)
        mainLayout.addWidget(actionFrame)

    def createIconFrame(self, MainWindow):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        iconLabel = QLabel()

        iconPath = Functions.set_svg_image("CSSCAN.svg")  # Functions 클래스를 사용하여 아이콘 경로를 가져옵니다.

        if os.path.isfile(iconPath):
            pixmap = QPixmap(iconPath)
            # 이미지를 적절한 비율로 조정합니다. 여기서는 원본 크기의 100%로 설정했습니다.
            scaleFactor = 1
            scaledPixmap = pixmap.scaled(pixmap.width() * scaleFactor, pixmap.height() * scaleFactor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            iconLabel.setPixmap(scaledPixmap)
        else:
            print(f"Failed to load icon: {iconPath}")

        iconLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(iconLabel)
        return frame

    def createSignInLabelFrame(self, MainWindow):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(1)  
        signInLabel = QLabel('SIGN IN TO CSSCAN')
        signInLabel.setAlignment(Qt.AlignCenter)
        signInLabel.setStyleSheet("font-size: 16px; color: white;")  
        layout.addWidget(signInLabel)
        userPassLabel = QLabel('Username or Email and password')
        userPassLabel.setAlignment(Qt.AlignCenter)
        userPassLabel.setStyleSheet("font-size: 12px; color: white;") 
        layout.addWidget(userPassLabel)
        return frame

    def createInputFrame(self, MainWindow):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        layout.setContentsMargins(30, 0, 30, 0)

        self.userEdit = PyLineEdit('Username or Email')
        self.userEdit.returnPressed.connect(self.onSignInClicked)
        # 특정 스타일 적용
        self.userEdit.setStyleSheet('''
            QLineEdit {
                background-color: #343b48; /* 배경색 */
                border-radius: 8px;
                padding: 5px 5px;
                color: #8a95aa; /* 텍스트 색상 */
            }
            QLineEdit:focus {
                border: 2px solid #343b48; /* 포커스 시 테두리 색상 */
                background-color: #2c313c; /* 포커스 시 배경색 */
            }
            QLineEdit::selection {
                color: #8a95aa; /* 선택 텍스트 색상 */
                background: #2c313c; /* 선택 배경 색상 */
            }
        ''')
        layout.addWidget(self.userEdit)

        self.passEdit = PyLineEdit('Password')
        self.passEdit.setEchoMode(QLineEdit.Password)
        self.passEdit.returnPressed.connect(self.onSignInClicked)
        # 동일한 스타일 적용
        self.passEdit.setStyleSheet(self.userEdit.styleSheet())
        layout.addWidget(self.passEdit)

        signInButton = PyPushButton('Sign in', MainWindow)
        signInButton.clicked.connect(self.onSignInClicked)
        # signInButton에 대한 스타일시트 확장
        additional_stylesheet = "QPushButton { background-color: #1b1e23; }"
        signInButton.setStyleSheet(signInButton.styleSheet() + additional_stylesheet)
        layout.addWidget(signInButton)

        return frame

    def createActionFrame(self, MainWindow):
        frame = QFrame()
        layout = QHBoxLayout(frame)

        layout.setContentsMargins(30, 0, 30, 0)

        forgetPassLabel = QLabel('Forget password?', MainWindow)  
        forgetPassLabel.setStyleSheet("font-size: 12px; color: white;")
        layout.addWidget(forgetPassLabel, 1)

        resetButton = PyResetButton('Reset Password', MainWindow) 
        resetButton.clicked.connect(self.onForgotPasswordClicked)
        layout.addWidget(resetButton, 1)
        return frame
    
    def onForgotPasswordClicked(self):
        self.forgot_passwd = PasswordResetModule()  
        self.forgot_passwd.show()

    def get_local_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception as e:
            print(f"Error obtaining IP address: {e}")
            return 'unknown'

    def onSignInClicked(self):
        username = self.userEdit.text()
        password = self.passEdit.text()
        ip_address = self.get_local_ip()

        # 데이터베이스 연결 가져오기
        db_connection = get_user_db_connection()
        auth_result = authenticate_user(username, password, ip_address, db_connection)
        
        if auth_result is not False:
            # UserManager 인스턴스를 가져와 현재 로그인한 사용자를 설정합니다.
            user_manager = UserManager.get_instance()
            user_manager.set_current_user(username)

            # 세션 관리자 초기화
            session_manager = SessionManager(db_connection)

            # 세션 ID 생성 (ip_address 인자 추가)
            session_id = session_manager.create_session(username, ip_address)

            # MainWindow 인스턴스 생성 시 username 전달
            self.main_window = MainWindow(session_id=session_id, username=username)
            
            # MainWindow 표시
            self.main_window.show()
            self.login_window.close()

            # 로그인 성공 메시지
            if auth_result == 'admin':
                success_msg = PyDialog('로그인 성공', '관리자로 성공적으로 로그인 하였습니다!')
            else:
                success_msg = PyDialog('로그인 성공', f'{username}님, 성공적으로 로그인 하였습니다!')
            success_msg.exec()

        else:
            fail_msg = PyDialog('로그인 실패', '사용자 이름 또는 비밀번호가 잘못되었습니다.')
            fail_msg.exec()
