import subprocess
import sys
import platform
import os
import shutil

def run_install_script():
    # 현재 스크립트의 디렉터리 경로
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if platform.system() == "Darwin":
        # macOS용 Bash 스크립트 실행
        script_path = os.path.join(script_dir, "postinstall")

        # Standalone 실행 파일을 애플리케이션 경로로 복사
        app_path = "/Applications/csscan.app/Contents/Resources/login"
        if not os.path.exists(app_path):
            os.makedirs(app_path)
        standalone_exe = os.path.join(script_dir,"create_admin_account")
        shutil.copy(standalone_exe, app_path)

        subprocess.run(["/bin/bash", script_path])

    elif platform.system() == "Windows":
        # Windows용 PowerShell 스크립트 실행
        script_path = os.path.join(script_dir, "postinstall.ps1")

        # Standalone 실행 파일을 애플리케이션 경로로 복사
        app_path = "C:\\Program Files (x86)\\csscan\\login"
        if not os.path.exists(app_path):
            os.makedirs(app_path)
        standalone_exe = os.path.join(script_dir, "create_admin_account.exe")
        shutil.copy(standalone_exe, app_path)

        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path])
    else:
        print("Unsupported operating system.")
        sys.exit(1)

if __name__ == "__main__":
    run_install_script()
