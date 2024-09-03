def check_func_5_1(client):
    no = "5_1"
    check_detail = "감사 로그 파일 접근 권한 점검: "
    check_result = "n/a"  # 초기 설정

    # 감사 로그 파일의 경로 설정 (환경에 맞게 조정 필요)
    audit_log_file_path = "/var/lib/mysql/audit.log"

    try:
        # 파일의 권한을 확인하는 명령어 실행
        stdin, stdout, stderr = client.exec_command(f"ls -l {audit_log_file_path}")
        output = stdout.read().decode('utf-8').strip()

        if output:
            permissions = output.split()[0]
            # 파일 권한이 소유자(read, write)에게만 허용되는지 확인
            if permissions.startswith('-rw-------'):
                check_detail += f"{audit_log_file_path} 파일의 접근 권한이 DBA(소유자)로 제한됨."
                check_result = "양호"
            else:
                check_detail += f"{audit_log_file_path} 파일의 접근 권한이 적절히 제한되지 않음."
                check_result = "취약"
        else:
            check_detail += f"{audit_log_file_path} 파일을 찾을 수 없음."
            check_result = "n/a"

    except Exception as e:
        check_detail += f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result