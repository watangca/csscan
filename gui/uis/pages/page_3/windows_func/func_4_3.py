import re

def check_func_4_3(client):
    no = "4_3"
    check_detail = ""
    check_result = "n/a"

    # 'Application' 로그의 최대 로그 크기 설정값을 확인하는 명령어
    cmd_max_log_size = "wevtutil gl Application | findstr maxSize"

    # 최대 로그 크기 확인
    result_max_log_size = client.run_ps(cmd_max_log_size)
    if result_max_log_size.status_code == 0:
        max_log_size_output = result_max_log_size.std_out.decode()
        max_log_size_match = re.search(r'\d+', max_log_size_output)
        if max_log_size_match:
            # 바이트 단위로 반환된 값을 KB로 변환
            max_log_size = int(max_log_size_match.group()) // 1024
            check_detail = f"최대 로그 크기 설정값: {max_log_size}KB"

            # 양호, 취약 판단
            if max_log_size >= 10240:
                check_result = "양호"
            else:
                check_result = "취약"

    return no, check_detail, check_result
