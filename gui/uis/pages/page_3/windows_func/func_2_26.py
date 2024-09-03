def check_func_2_26(client):
    no = "2_26"
    check_detail = "터미널 서비스 최소 암호화 수준: "
    check_result = "n/a"

    try:
        # MinEncryptionLevel 값 확인
        encryption_level_cmd = "(Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp').MinEncryptionLevel"
        encryption_level_result = client.run_ps(encryption_level_cmd)

        if encryption_level_result.status_code == 0:
            encryption_level = encryption_level_result.std_out.decode('utf-8').strip()
            check_detail += encryption_level

            if not encryption_level or int(encryption_level) >= 2:
                check_result = "양호"  # 사용하지 않거나, 중간 이상의 암호화 수준
            elif int(encryption_level) == 1:
                check_result = "취약"  # 낮은 암호화 수준
            else:
                check_result = "n/a"
        else:
            check_detail += "암호화 수준 확인 실패: " + encryption_level_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
