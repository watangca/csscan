import datetime
import re

def check_func_3_1(client):
    no = "3_1"
    ps_script = "Get-HotFix | Select-Object -Property Description, HotFixID, InstalledOn | Format-Table -AutoSize"
    response = client.run_ps(ps_script)

    if response.status_code != 0:
        return no, "n/a", "n/a"

    hotfixes_str = response.std_out.decode()
    check_detail = hotfixes_str.strip()

    latest_patch_date = None
    for line in hotfixes_str.splitlines():
        if 'InstalledOn' in line or '---' in line or line.strip() == '':
            continue  # 헤더 라인, 구분선, 빈 라인 건너뛰기
        parts = line.split()
        try:
            # 날짜 정보 추출 및 파싱
            date_str = ' '.join(parts[-3:])  # 마지막 세 부분을 합쳐서 날짜 문자열을 형성
            patch_date = datetime.datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
            if latest_patch_date is None or patch_date > latest_patch_date:
                latest_patch_date = patch_date
        except (ValueError, IndexError):
            continue  # 날짜 파싱 실패 또는 부적절한 라인인 경우 건너뛰기

    check_result = "n/a"
    if latest_patch_date:
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
        if latest_patch_date > one_year_ago:
            check_result = "양호"
        else:
            check_result = "취약"

    return no, check_detail, check_result
