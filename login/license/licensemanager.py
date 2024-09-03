import os
import sys
import json
import uuid
import shutil
import subprocess
import platform
from cryptography.fernet import Fernet

def determine_license_path(license_dirname, license_filename, key_filename):
    app_name = "CSSCAN"
    if getattr(sys, 'frozen', False):
        # PyInstaller 실행 환경일 경우
        # 데이터를 사용자의 AppData (Windows) 또는 Application Support (macOS) 디렉토리로 복사
        app_data_dir = os.getenv('LOCALAPPDATA') if os.name == 'nt' else os.path.expanduser('~/Library/Application Support')
        dest_folder = os.path.join(app_data_dir, app_name, license_dirname)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        license_path = os.path.join(dest_folder, license_filename)
        key_path = os.path.join(dest_folder, key_filename)

        # 복사되지 않았다면, 실행 파일과 동일한 디렉토리에서 라이센스 파일을 복사
        if not os.path.exists(license_path) or not os.path.exists(key_path):
            # 'login/license' 경로 수정
            src_license_path = os.path.join(sys._MEIPASS, 'login/license', license_filename)
            src_key_path = os.path.join(sys._MEIPASS, 'login/license', key_filename)
            shutil.copy(src_license_path, license_path)
            shutil.copy(src_key_path, key_path)
    else:
        # 개발 환경일 경우, 프로젝트 내의 라이센스 디렉토리 사용
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        license_dir = os.path.join(project_dir, 'license')  # 'login/license' 경로로 수정
        license_path = os.path.join(license_dir, license_filename)
        key_path = os.path.join(license_dir, key_filename)

    return license_path, key_path

def load_license_file(license_path, key_path):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        with open(license_path, 'rb') as license_file:
            encrypted_data = license_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        license_info = json.loads(decrypted_data.decode('utf-8'))
        return license_info
    except Exception as e:
        print(f"라이센스 파일 로딩 오류: {e}")
        return None   
    
def get_hardware_id():
    # 컴퓨터의 MAC 주소를 얻는 함수
    mac = uuid.getnode()
    mac_str = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_str

def get_cpu_id():
    # 시스템 운영 체제에 따라 CPU ID를 가져오는 함수
    try:
        if platform.system() == "Windows":
            cmd = 'wmic cpu get ProcessorId'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            cpu_id = stdout.decode().split('\n')[1].strip()
        elif platform.system() == "Darwin":
            cmd = 'sysctl -n machdep.cpu.brand_string'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            cpu_id = stdout.decode().strip()
        else:
            cpu_id = "Unsupported OS"
    except Exception as e:
        print(f"Error fetching CPU ID: {e}")
        cpu_id = "Error"
    return cpu_id