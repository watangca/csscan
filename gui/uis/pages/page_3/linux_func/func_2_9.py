import subprocess

def check_func_2_9(client):
    no = "2_9"
    check_file_list = [
        "/sbin/dump",
        "/sbin/restore",
        "/sbin/unix_chkpwd",
        "/usr/bin/at",
        "/usr/bin/lpq",
        "/usr/bin/lpq-lpd",
        "/usr/bin/lpr",
        "/usr/bin/lpr-lpd",
        "/usr/bin/lprm",
        "/usr/bin/lprm-lpd",
        "/usr/bin/newgrp",
        "/usr/sbin/lpc",
        "/usr/sbin/lpc-lpd",
        "/usr/sbin/traceroute"
    ]

    check_result = "양호"  
    vulnerable_files = []

    for file_path in check_file_list:
        try:
            command = f"ls -alL {file_path} | awk '{{ print $1 }}' | grep -i 's'"
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.stdout:
                check_result = "취약"
                vulnerable_files.append((file_path, result.stdout))

        except Exception as e:
            print(f"오류 발생: {e}")

    # 취약한 파일 목록과 상세 정보 출력
    if check_result == "취약":
        check_detail = "\n".join([f"{file_path}: {output.strip()}" for file_path, output in vulnerable_files])
    else:
        check_detail = "취약한 파일이 발견되지 않음"

    return no, check_detail, check_result