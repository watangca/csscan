import json

def check_func_2_8(client):
    no = "2_8"
    check_detail = "IIS 가상 디렉토리 존재 여부: "
    check_result = "n/a"

    # IISSamples, IISHelp 가상 디렉토리 존재 여부를 확인하는 PowerShell 명령어
    ps_command = """
    $virtualDirs = @('IISSamples', 'IISHelp')
    $site = Get-WebSite | Select-Object -First 1
    $foundDirs = foreach ($dir in $virtualDirs) {
        $path = "IIS:\\Sites\\$($site.Name)\\$dir"
        if (Test-Path $path) {
            $dir
        }
    }
    $result = @{
        'FoundDirs' = $foundDirs -join ', '
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)

        foundDirs = data['FoundDirs']
        check_detail += f"발견된 가상 디렉토리: {foundDirs if foundDirs else '없음'}"

        if foundDirs:
            check_result = "취약"
        else:
            check_result = "양호"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result
