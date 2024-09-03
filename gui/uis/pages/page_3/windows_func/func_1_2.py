def check_func_1_2(client):
    no = "1_2"
    check_detail = ""
    check_result = ""

    # Guest 계정을 확인하고, 계정 사용 안함 설정 여부를 확인
    try:
        # 원격 서버에서 Guest 계정의 상태 정보를 가져옴
        result = client.run_ps("Get-LocalUser -Name 'Guest' | Select-Object -ExpandProperty 'Enabled'")
        
        # Guest 계정이 사용 안함으로 설정되어 있는 경우
        if result.status_code == 0 and result.std_out.strip() == "False":
            check_detail = "Guest 계정이 비활성화 되어 있음"
            check_result = "양호"
        # Guest 계정이 사용 안함으로 설정되지 않은 경우
        else:
            check_detail = "Guest 계정이 활성화 되어 있음"
            check_result = "취약"
    except Exception as e:
        check_detail = f"Guest 계정 상태 확인 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result