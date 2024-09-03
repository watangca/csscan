def check_func_1_12(client):
    no = "1_12"
    check_detail = "패스워드 최소 사용기간 설정 값: "
    check_result = "n/a"

    try:
        # 보안 정책 중 'Minimum Password Age' 설정 조회
        password_age_command = """
        secedit /export /cfg C:\\temp\\secpol.cfg
        Get-Content -Path C:\\temp\\secpol.cfg | Select-String -Pattern "MinimumPasswordAge"
        """
        password_age_response = client.run_ps(password_age_command)

        if password_age_response.status_code == 0 and password_age_response.std_out:
            output = password_age_response.std_out.decode('utf-8').strip()
            # 결과에서 패스워드 최소 사용기간 값 추출
            minimum_password_age = next((line.split('=')[1].strip() for line in output.split('\n') if "MinimumPasswordAge" in line), None)
            if minimum_password_age is not None:
                check_detail += minimum_password_age
                # 패스워드 최소 사용기간이 0보다 큰 경우 '양호', 0인 경우 '취약'
                if int(minimum_password_age) > 0:
                    check_result = "양호"
                else:
                    check_result = "취약"
            else:
                check_detail += "설정 값을 찾을 수 없음"
        else:
            check_detail += "패스워드 최소 사용기간 설정을 확인할 수 없음: " + password_age_response.std_err.decode('utf-8').strip()

    except Exception as e:
        check_detail += f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result

