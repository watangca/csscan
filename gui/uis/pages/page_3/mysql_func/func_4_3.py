def check_func_4_3(mysql_conn):
    no = "4_3"
    check_result = "양호"  # 기본값을 "양호"로 설정

    # MySQL 서버의 현재 버전을 확인
    try:
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()

        if version:
            current_version = version[0]
            check_detail = f"현재 MySQL 서버 버전: {current_version}, "
        else:
            check_detail = "버전 정보를 조회할 수 없습니다.\n"

    except Exception as e:
        check_detail = f"버전 확인 중 오류 발생: {e}\n"

    # 사용자가 직접 최신 패치 적용 여부를 입력할 수 있는 부분
    # 이 부분은 사용자가 최신 버전 정보를 확인하고 수동으로 작성해야 합니다.
    # 예: "최신 버전: 8.0.25, 적용된 패치: 8.0.23 - 업데이트 필요"
    # 실제 사용 시에는 아래의 텍스트를 최신 상태에 맞게 업데이트해야 합니다.
    user_input_latest_patch_info = "현재 버전정보와 mysql 최신패치를 확인하고, 적용 영향도 평가를 실시하여 적용여부를 판단해야함"

    # 최종적으로 점검 내용에 사용자 입력 부분을 추가
    check_detail += user_input_latest_patch_info

    return no, check_detail, check_result