def check_func_1_6(client):
    no = "1_6"
    check_detail = ""
    check_result = "n/a"

    # PowerShell 명령어를 사용하여 Administrators 그룹의 구성원 목록 확인
    ps_command = "Get-LocalGroupMember -Group 'Administrators' | Select-Object -ExpandProperty Name"

    try:
        # 원격 서버에서 Administrators 그룹의 구성원 목록 가져옴
        result = client.run_ps(ps_command)

        if result.status_code == 0:
            # 구성원 목록 추출 및 형식화
            admin_members = result.std_out.decode().splitlines()

            # 구성원 수와 목록을 상세 정보에 추가
            check_detail += f"Administrators 그룹 내의 계정 갯수: {len(admin_members)}명, 계정: {', '.join(admin_members)}"

            # 구성원 수에 따라 결과 설정
            if len(admin_members) <= 1:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "Administrators 그룹의 목록을 확인하는 데 실패했습니다."

    except Exception as e:
        check_detail += f"구성원 목록 확인 중 오류 발생: {str(e)}"

    return no, check_detail, check_result
