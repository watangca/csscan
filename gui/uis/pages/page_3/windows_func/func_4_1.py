def check_func_4_1(client):
    no = "4_1"
    check_detail = "Security 로그 검사 결과: \n"

    # PowerShell 명령을 사용하여 Security 로그의 오류 또는 경고 이벤트 검색
    ps_script = """
    Get-EventLog -LogName Security -EntryType Error,Warning -Newest 10 | Format-List
    """
    result = client.run_ps(ps_script)

    # 결과를 디코딩하고 파싱
    std_out = result.std_out.decode('utf-8') if result.std_out else ""
    std_err = result.std_err.decode('utf-8') if result.std_err else ""

    # "No matches found" 메시지가 std_err에 있는 경우 '양호'로 판단
    if "No matches found" in std_err:
        check_detail += "Security 이벤트 로그에서 오류 또는 경고 이벤트가 발견되지 않음"
        check_result = "양호"
    elif std_err:
        # 다른 종류의 오류 발생 시
        check_detail += "오류 발생: " + std_err.strip()
        check_result = "n/a"
    elif std_out.strip():
        # 문제가 있는 로그의 내용을 추가
        check_detail += std_out.strip()
        check_result = "취약"
    else:
        # std_out에 유효한 내용이 없는 경우
        check_detail += "Security 로그 검사 결과를 확인할 수 없음"
        check_result = "n/a"

    return no, check_detail, check_result
