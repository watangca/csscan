def check_func_2_25(client):
    no = "2_25"
    check_detail = "Windows Server 버전: "
    check_result = "n/a"

    try:
        # 운영 체제 버전 확인
        os_version_cmd = "(Get-WmiObject -Class Win32_OperatingSystem).Version"
        os_version_result = client.run_ps(os_version_cmd)

        if os_version_result.status_code == 0:
            os_version = os_version_result.std_out.decode('utf-8').strip()
            check_detail += os_version

            # Windows Server 2019 이상인지 확인
            if os_version.startswith("10.0."):
                build_number = int(os_version.split('.')[2])
                if build_number >= 17763:  # Windows Server 2019의 빌드 번호
                    check_result = "양호"
                else:
                    check_result = "취약"
            else:
                check_result = "취약"
        else:
            check_detail += "OS 버전 확인 실패: " + os_version_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
