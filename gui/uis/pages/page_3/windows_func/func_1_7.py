def check_func_1_7(client):
    no = "1_7"
    check_detail = "Everyone 사용권한 익명 사용자 적용 점검: "
    check_result = "n/a"

    # PowerShell 명령어를 사용하여 정책 설정 확인
    ps_command = "Get-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Lsa' -Name 'EveryoneIncludesAnonymous' | Select-Object -ExpandProperty EveryoneIncludesAnonymous"

    try:
        # 원격 서버에서 정책 값을 가져옴
        result = client.run_ps(ps_command)

        if result.status_code == 0:
            # 정책 값 추출
            policy_value = result.std_out.decode().strip()

            # 정책 값에 따라 결과 설정 및 상세 정보 업데이트
            if policy_value == "0":
                check_result = "양호"
                check_detail += "사용 안 함 (현재 설정값: 0)"
            elif policy_value == "1":
                check_result = "취약"
                check_detail += "사용 (현재 설정값: 1)"
            else:
                check_detail += f"해당 정책의 상태를 확인할 수 없습니다 (현재 설정값: {policy_value})."
        else:
            check_detail += "해당 정책의 상태를 확인하는 데 실패했습니다."

    except Exception as e:
        check_detail += f"정책 확인 중 오류 발생: {str(e)}"

    return no, check_detail, check_result
