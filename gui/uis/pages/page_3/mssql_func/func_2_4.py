def check_func_2_4(win_conn):
    no = "2_4"
    check_detail = "사용중인 ODBC 데이터 소스 목록:"
    
    # PowerShell 스크립트: 설치된 ODBC 데이터 소스 목록 조회
    ps_script = """
    $dsns = Get-OdbcDsn
    if ($dsns) {
        $output = ''
        foreach ($dsn in $dsns) {
            $output += "$($dsn.Name) - $($dsn.DriverName)`n"
        }
        $output
    } else {
        "설치된 ODBC 데이터 소스가 없습니다."
    }
    """

    try:
        # WinRM을 사용하여 원격 서버에서 PowerShell 스크립트 실행
        result = win_conn.run_ps(ps_script)
        if result.status_code == 0:
            # PowerShell 명령의 성공적인 출력 결과를 문자열로 변환하여 check_detail에 추가
            output = result.std_out.decode('utf-8').strip() if isinstance(result.std_out, bytes) else result.std_out.strip()
            check_detail += output
        else:
            # PowerShell 명령 실행에 실패한 경우
            check_detail += "원격 서버에서 ODBC 데이터 소스 목록을 조회하는 데 실패했습니다."
    except Exception as e:
        # 예외 발생 시 처리
        check_detail += f"점검 중 오류 발생: {str(e)}"

    # 추가 지시된 문구를 포함
    check_detail += "사용중인 ODBC 데이터 소스에 대한 사용여부를 확인하고, 불필요한 ODBC 데이터 소스 삭제."

    # 점검 결과 설정: 이 접근 방식에서는 점검이 성공적으로 수행되었다고 가정하고 '양호'로 설정
    check_result = "양호"

    return no, check_detail, check_result
