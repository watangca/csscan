import smtplib
import random
import string
from . import smtp_config
from qt_core import *
from gui.widgets import *
from email.mime.text import MIMEText
from login.auth_module import hash_password
from login.database.UserDatabaseManager import get_user_db_connection

class PasswordResetModule(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Password Reset')
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("background-color: #21252d;")

        layout = QVBoxLayout()

        self.accountLineEdit = PyLineEdit("Username or Email")
        layout.addWidget(self.accountLineEdit)

        self.verificationCodeLineEdit = PyLineEdit("Verification code")
        layout.addWidget(self.verificationCodeLineEdit)

        self.resetButton = PyPushButton('Get verification code', self)
        self.resetButton.clicked.connect(self.onVerificationRequested)
        layout.addWidget(self.resetButton)

        self.verifyButton = PyPushButton('Password reset', self)
        self.verifyButton.clicked.connect(self.onResetConfirmed)
        layout.addWidget(self.verifyButton)

        self.setLayout(layout)

    def onVerificationRequested(self):
        try:
            account_info = self.accountLineEdit.text()
            email = self.retrieve_email(account_info)
            if email:
                self.verification_code = self.generate_verification_code()
                self.send_verification_email(email, self.verification_code)
                PyDialog.information(self, "인증번호 발송", "인증번호가 이메일로 전송되었습니다.")
            else:
                PyDialog.warning(self, "오류", "계정을 찾을 수 없습니다.")
        except Exception as e:
            print(f"Error in onVerificationRequested: {e}")

    def onResetConfirmed(self):
        input_code = self.verificationCodeLineEdit.text()
        if input_code == self.verification_code:
            new_password = self.generate_new_password()
            account_info = self.accountLineEdit.text()
            email = self.retrieve_email(account_info)
            self.update_password(account_info, new_password)
            self.send_new_password_email(email, new_password)
            PyDialog.information(self, "비밀번호 재설정 완료", "새 비밀번호가 이메일로 전송되었습니다.")
            self.close()
        else:
            PyDialog.warning(self, "오류", "잘못된 인증번호입니다.")

    def retrieve_email(self, account_info):
        conn = get_user_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM users WHERE username = ? OR email = ?', (account_info, account_info))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def generate_verification_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def generate_new_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def update_password(self, username, new_password):
        """새 비밀번호로 사용자 비밀번호를 업데이트합니다."""
        hashed_password = hash_password(new_password)  # 새 비밀번호 해시 처리
        try:
            conn = get_user_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
            conn.commit()
            print("비밀번호가 성공적으로 업데이트되었습니다.")
        except Exception as e:
            print(f"비밀번호 업데이트 중 오류가 발생했습니다: {e}")
        finally:
            conn.close()

    def send_email(self, to_email, subject, content):
        # smtp_config.py에서 설정을 직접 사용
        smtp_server = smtp_config.SMTP_SERVER
        smtp_port = smtp_config.SMTP_PORT
        smtp_user = smtp_config.SMTP_USER
        smtp_password = smtp_config.SMTP_PASSWORD

        message = MIMEText(content)
        message['Subject'] = subject
        message['From'] = smtp_user
        message['To'] = to_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # TLS 사용
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, [to_email], message.as_string())
        except Exception as e:
            print(f"이메일 전송 중 오류가 발생했습니다: {e}")

    def send_verification_email(self, email, code):
        subject = '비밀번호 재설정 인증번호'
        content = f"귀하의 인증번호는 {code} 입니다."
        self.send_email(email, subject, content)

    def send_new_password_email(self, email, new_password):
        subject = '귀하의 새 비밀번호'
        content = f"귀하의 새 비밀번호는 {new_password} 입니다."
        self.send_email(email, subject, content)
