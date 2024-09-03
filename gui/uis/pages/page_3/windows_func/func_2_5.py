import json

def check_func_2_5(client):
    no = "2_5"
    check_detail = "IIS 웹서버 디렉토리 검색 설정: "
    check_result = "n/a"

    # IIS 서비스 상태 및 디렉토리 검색 설정 확인을 위한 PowerShell 명령어
    ps_command = """
    $iisService = Get-Service -Name 'W3SVC' -ErrorAction SilentlyContinue
    if ($iisService -and $iisService.Status -eq 'Running') {
        $directoryBrowsing = Get-WebConfigurationProperty -Filter '/system.webServer/directoryBrowse' -PSPath 'MACHINE/WEBROOT/APPHOST' -Name 'enabled'
        $result = @{
            'ServiceRunning' = $true
            'DirectoryBrowsingEnabled' = $directoryBrowsing.Value
        }
    } else {
        $result = @{
            'ServiceRunning' = $false
            'DirectoryBrowsingEnabled' = $false
        }
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)

        if data['ServiceRunning']:
            check_detail += f"구동 중, 디렉토리 검색 서비스 활성화: {data['DirectoryBrowsingEnabled']}"
            if data['DirectoryBrowsingEnabled']:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail += "IIS 서비스가 구동중이지 않음"
            check_result = "양호"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result
