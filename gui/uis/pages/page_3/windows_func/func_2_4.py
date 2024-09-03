import json

def check_func_2_4(client):
    no = "2_4"
    check_detail = "IIS 웹서버 상태: "
    check_result = "n/a"

    # IIS 서비스와 버전, 기본 페이지 확인을 위한 PowerShell 명령어
    ps_command = """
    $iisService = Get-Service -Name 'W3SVC' -ErrorAction SilentlyContinue
    if ($iisService -and $iisService.Status -eq 'Running') {
        $version = Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\InetStp\\' -Name 'VersionString' -ErrorAction SilentlyContinue
        $defaultPage = (Test-Path 'C:\\inetpub\\wwwroot\\iisstart.htm') -or (Test-Path 'C:\\inetpub\\wwwroot\\index.*')
        $result = @{
            'Version' = $version.VersionString
            'UsingDefaultPage' = $defaultPage
        }
    } else {
        $result = @{
            'Version' = 'Not Running'
            'UsingDefaultPage' = $false
        }
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)

        if data['Version'] != 'Not Running':
            check_detail += f"IIS 버전: {data['Version']}, "
            if data['UsingDefaultPage']:
                check_detail += "IIS 기본페이를 사용중"
                check_result = "취약"
            else:
                check_detail += "IIS 기본페이지를 사용하지 않음"
                check_result = "양호"
        else:
            check_detail += "IIS 서비스가 구동중이지 않음."
            check_result = "양호"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result
