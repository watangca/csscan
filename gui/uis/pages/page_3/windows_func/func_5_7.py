def check_func_5_7(client):
    no = "5_7"
    check_detail = "네트워크 액세스 설정 확인: "
    check_result = "n/a"

    # 원격 시스템에서 해당 정책 확인을 위한 PowerShell 명령어
    policy_command = """
    $registryPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters"
    $properties = @("RestrictNullSessAccess", "RestrictAnonymousSAM")
    $values = @{}

    foreach ($property in $properties) {
        try {
            $value = (Get-ItemProperty -Path $registryPath -Name $property).$property
            $values[$property] = $value
        } catch {
            $values[$property] = "Not Found"
        }
    }

    return $values
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            # 출력 파싱하여 설정값 확인
            output = policy_response.std_out.decode('utf-8').strip()
            restrict_null_sess_access = "1" if "RestrictNullSessAccess=1" in output else "0"
            restrict_anonymous_sam = "1" if "RestrictAnonymousSAM=1" in output else "0"

            check_detail += f"SAM 계정과 공유의 익명 열거 허용 안 함: {restrict_null_sess_access}, SAM 계정의 익명 열거 허용 안 함: {restrict_anonymous_sam}"

            # 정책 검사
            if restrict_null_sess_access == "1" and restrict_anonymous_sam == "1":
                check_result = "양호"
            elif restrict_null_sess_access == "0" or restrict_anonymous_sam == "0":
                check_result = "취약"
            else:
                check_result = "n/a"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"

    return no, check_detail, check_result
