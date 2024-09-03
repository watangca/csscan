def check_func_1_18(client):
    no = "1_18"

    # PowerShell 명령으로 Remote Desktop Users 그룹의 멤버 가져오기
    ps_script = """
    $group = [ADSI]("WinNT://$env:COMPUTERNAME/Remote Desktop Users,group")
    @($group.Invoke("Members")) | foreach {
        $_.GetType().InvokeMember("Name", 'GetProperty', $null, $_, $null)
    }
    """

    try:
        # 클라이언트를 통해 PowerShell 명령 실행
        response = client.run_ps(ps_script)

        if response.status_code == 0:
            # PowerShell 명령 결과 처리
            members = response.std_out.decode().strip().split('\r\n')
            members = [member.strip() for member in members if member.strip()]

            # 체크 결과와 상세 정보 설정
            if "Administrator" not in members or len(members) == 1:
                check_result = "취약"
            else:
                check_result = "양호"

            check_detail = "원격 터미널 사용 가능 계정: " + ", ".join(members) if members else "원격 터미널 사용 가능 계정 없음"
        else:
            check_detail = "원격 명령 실행 실패"
            check_result = "n/a"
    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
