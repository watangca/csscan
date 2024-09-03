import json

def check_func_2_2(client):
    no = "2_2"
    check_detail = "하드디스크 기본 공유 설정: "
    check_result = "n/a"

    # 레지스트리 키와 기본 공유를 확인하는 PowerShell 명령어
    ps_command = """
    $regPath = 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\lanmanserver\\parameters'
    $regKeys = @('AutoShareServer', 'AutoShareWks')
    $regValues = @{}
    foreach ($key in $regKeys) {
        $value = (Get-ItemProperty -Path $regPath -Name $key -ErrorAction SilentlyContinue).$key
        if ($null -ne $value) {
            $regValues[$key] = $value
        }
    }

    $shares = net share | Out-String
    $defaultShares = @('ADMIN$', 'C$', 'D$', 'IPC$') # 기본 공유 목록
    $foundShares = $defaultShares | Where-Object { $shares -like "*$_*" } | ForEach-Object { $_ }

    $result = @{
        'regValues' = $regValues
        'foundShares' = $foundShares -join ', '
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)
        regValues = data["regValues"]
        foundShares = data["foundShares"]

        regValuesOutput = "설정값 찾을 수 없음" if not regValues else json.dumps(regValues)
        check_detail += f"레지스트리 값: {regValuesOutput}, 기본 공유 폴더: {foundShares if foundShares else '없음'}"

        # 레지스트리 값과 기본 공유 존재 여부에 따라 결과 분석
        if (not regValues or 0 in regValues.values()) and not foundShares:
            check_result = "양호"
        else:
            check_result = "취약"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()

    return no, check_detail, check_result
