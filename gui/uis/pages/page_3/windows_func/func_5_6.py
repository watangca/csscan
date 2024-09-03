def check_func_5_6(client):
    no = "5_6"
    check_detail = "보안 감사를 로그할 수 없는 경우 즉시 시스템 종료 설정값: "
    check_result = "n/a"

    # 원격 시스템에서 해당 정책 확인을 위한 PowerShell 명령어
    policy_command = """
    Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa' -Name 'CrashOnAuditFail'
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            # 출력에서 'CrashOnAuditFail' 값 추출
            output_lines = policy_response.std_out.decode('utf-8').split('\n')
            crash_on_audit_fail_line = next((line for line in output_lines if "crashonauditfail" in line.lower()), None)

            if crash_on_audit_fail_line:
                value = crash_on_audit_fail_line.split(":")[1].strip()
                check_detail += value

                # 정책 검사
                if value == "0":
                    check_result = "양호"
                elif value == "1":
                    check_result = "취약"
                else:
                    check_result = "n/a"
            else:
                check_result = "n/a"
                check_detail += "정책 값 찾을 수 없음"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"

    return no, check_detail, check_result
