import json

def check_func_2_7(client):
    no = "2_7"
    check_detail = "IIS 상위 디렉토리 접근 설정: "
    check_result = "n/a"

    # IIS 상위 디렉토리 접근 설정을 확인하는 PowerShell 명령어
    ps_command = """
    $parentPaths = Get-WebConfigurationProperty -Filter '/system.webServer/asp' -PSPath 'MACHINE/WEBROOT/APPHOST' -Name 'enableParentPaths'
    $result = @{
        'ParentPathsEnabled' = $parentPaths.Value
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)

        check_detail += f"부모 경로 사용 체크: {data['ParentPathsEnabled']}"

        if data['ParentPathsEnabled']:
            check_result = "취약"
        else:
            check_result = "양호"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result
