def check_func_1_1(client):
    no = "1_1"

    # 관리자 그룹에 속한 계정 확인을 위한 명령
    check_command = "net localgroup Administrators"
    result = client.run_ps(check_command)

    # 결과 분석 및 점검
    if result.status_code == 0:
        output = result.std_out.decode('utf-8')
        if "Administrator" in output:
            check_detail = "관리자 그룹에 'Administrator' 계정이 존재함(계정명 변경필요)"
            check_result = "취약"
        else:
            check_detail = "관리자 그룹에 'Administrator' 계정이 존재하지 않음"
            check_result = "양호"
    else:
        check_detail = "점검 실패: 결과를 확인할 수 없음"
        check_result = "n/a"

    return no, check_detail, check_result
