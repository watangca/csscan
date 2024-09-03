import os
import sys
import sqlite3
import shutil
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_filename="csscan_db.db"):
        self.db_path = self.determine_db_path(db_filename)
        self.conn = self.create_connection()
        self.create_tables()

    def determine_db_path(self, db_filename):
        app_name = "CSSCAN"
        if getattr(sys, 'frozen', False):
            dest_folder = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            database_path = os.path.join(dest_folder, db_filename)

            if not os.path.exists(database_path):
                src_db_path = os.path.join(sys._MEIPASS, 'gui/database', db_filename)
                shutil.copy(src_db_path, database_path)
        else:
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            database_path = os.path.join(project_dir, 'database', db_filename)

        return database_path

    def create_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_tables(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                tables = [
                    """
                    CREATE TABLE IF NOT EXISTS linux_data (
                        ID INTEGER PRIMARY KEY,
                        NO INTEGER NOT NULL UNIQUE,
                        IP_ADDRESS TEXT NOT NULL,
                        OS TEXT,
                        STATUS TEXT,
                        CHECK_DATE TEXT
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS windows_data (
                        ID INTEGER PRIMARY KEY,
                        NO INTEGER NOT NULL UNIQUE,
                        IP_ADDRESS TEXT NOT NULL,
                        OS TEXT,
                        STATUS TEXT,
                        CHECK_DATE TEXT
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS database_data (
                        ID INTEGER PRIMARY KEY,
                        NO INTEGER NOT NULL UNIQUE,
                        IP_ADDRESS TEXT NOT NULL,
                        OS TEXT,
                        STATUS TEXT,
                        CHECK_DATE TEXT
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS linux_checklist (
                        NO TEXT,
                        CATEGORY TEXT,
                        CHECK_LIST TEXT,
                        SEVERITY TEXT,
                        GUIDE TEXT,
                        CHECK_DETAIL REAL,
                        CHECK_RESULT REAL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS windows_checklist (
                        NO TEXT,
                        CATEGORY TEXT,
                        CHECK_LIST TEXT,
                        SEVERITY TEXT,
                        GUIDE TEXT,
                        CHECK_DETAIL REAL,
                        CHECK_RESULT REAL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS database_checklist (
                        NO TEXT,
                        CATEGORY TEXT,
                        CHECK_LIST TEXT,
                        SEVERITY TEXT,
                        GUIDE TEXT,
                        CHECK_DETAIL REAL,
                        CHECK_RESULT REAL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS report_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        template TEXT NOT NULL,
                        target TEXT NOT NULL,
                        date TEXT NOT NULL,
                        status TEXT NOT NULL
                    )
                    """
                ]
                for table in tables:
                    cursor.execute(table)
        except Error as e:
            raise e

    def renumber_no_column(self, table):
        self.validate_table(table)
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT ID FROM {table} ORDER BY NO")
                ids = [row[0] for row in cursor.fetchall()]
                for new_no, id_ in enumerate(ids, start=1):
                    cursor.execute(f"UPDATE {table} SET NO = ? WHERE ID = ?", (new_no, id_))
        except Error as e:
            raise e

    def validate_table(self, table):
        valid_tables = ["linux_data", "windows_data", "database_data"]
        if table not in valid_tables and not table.endswith("_checklist"):
            raise ValueError(f"Unknown table: {table}")

    def get_data_count(self, table):
        self.validate_table(table)
        query = f"SELECT COUNT(*) FROM {table}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"데이터 개수 조회 중 오류가 발생했습니다: {e}")
            return 0

    def save_single_data(self, table, data):
        self.validate_table(table)
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT MAX(NO) FROM {table}")
        last_no = cursor.fetchone()[0]
        new_no = last_no + 1 if last_no else 1

        if table in ["linux_data", "windows_data", "database_data"]:
            sql = f'''INSERT INTO {table}(NO, IP_ADDRESS, OS, STATUS, CHECK_DATE) VALUES(?, ?, ?, ?, NULL)'''
        data = (new_no,) + data
        try:
            with self.conn:
                cursor.execute(sql, data)
        except Error as e:
            raise e

    def delete_single_data(self, table, ip_address):
        self.validate_table(table)
        sql = f"DELETE FROM {table} WHERE IP_ADDRESS=?"

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(sql, (ip_address,))
        except Error as e:
            raise e

    def delete_check_table_for_ip(self, ip_address, table_type):
        if table_type == 'windows':
            prefix = 'windows'
        elif table_type == 'linux':
            prefix = 'linux'
        elif table_type == 'database':
            prefix = 'database'
        else:
            raise ValueError("Unknown table type")

        table_name = f"{prefix}_{ip_address.replace('.', '_')}"
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if cursor.fetchone():
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    print(f"Deleted check table for IP: {table_name}")
        except Error as e:
            print(f"Failed to delete check table for IP {ip_address}: {e}")

    def fetch_all_data(self, table):
        self.validate_table(table)
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            return cursor.fetchall()
        except Error as e:
            raise e

    def update_checklist(self, checklist_type, no, ip_address, check_detail, check_result):
        print(f"Updating {checklist_type} checklist for IP_ADDRESS: {ip_address}")
        try:
            with self.conn:
                cursor = self.conn.cursor()
                table_name = f"{checklist_type}_{ip_address.replace('.', '_')}"
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY, NO TEXT NOT NULL UNIQUE, CHECK_DETAIL TEXT, CHECK_RESULT TEXT)")

                cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE NO=?", (no,))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.execute(f"UPDATE {table_name} SET CHECK_DETAIL=?, CHECK_RESULT=? WHERE NO=?", (check_detail, check_result, no))
                else:
                    cursor.execute(f"INSERT INTO {table_name} (NO, CHECK_DETAIL, CHECK_RESULT) VALUES (?, ?, ?)", (no, check_detail, check_result))
        except Error as e:
            print(f"Error updating table {table_name}: {e}")
            raise e

    def fetch_detail_data(self, checklist_type, ip_address):
        try:
            cursor = self.conn.cursor()
            table_name = f"{checklist_type}_{ip_address.replace('.', '_')}"
            query = f"""
            SELECT c.NO, c.CATEGORY, c.CHECK_LIST, c.SEVERITY, d.CHECK_DETAIL, d.CHECK_RESULT
            FROM {checklist_type}_checklist c
            LEFT JOIN {table_name} d ON c.NO = d.NO
            """
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.OperationalError as e:
            return []
        except Error as e:
            print(f"Error fetching detail data: {e}")
            return []

    def fetch_data_for_ip(self, table, ip_address):
        self.validate_table(table)
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE IP_ADDRESS=?", (ip_address,))
            return cursor.fetchone()
        except Error as e:
            raise e

    def fetch_check_date(self, table, ip):
        self.validate_table(table)
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT CHECK_DATE FROM {table} WHERE IP_ADDRESS=?", (ip,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Error as e:
            raise e

    def update_check_date(self, table, ip, check_date):
        self.validate_table(table)
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"UPDATE {table} SET CHECK_DATE = ? WHERE IP_ADDRESS=?", (check_date, ip))
        except Error as e:
            raise e

    def fetch_completed_checks(self, table):
        self.validate_table(table)
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT NO, IP_ADDRESS, OS, CHECK_DATE FROM {table} WHERE CHECK_DATE IS NOT NULL")
                return cursor.fetchall()
        except Error as e:
            raise e

    def fetch_completed_ips(self, table):
        self.validate_table(table)
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT ip_address FROM {table} WHERE CHECK_DATE IS NOT NULL")
                return cursor.fetchall()
        except Error as e:
            raise e

    def fetch_check_results(self, query_table):
        cursor = self.conn.cursor()
        query = f"SELECT NO, CHECK_RESULT FROM {query_table}"
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def fetch_check_count(self, table):
        self.validate_table(table)
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE CHECK_DATE IS NOT NULL")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Error as e:
            raise e

    def fetch_vulnerability_count_by_ip(self, system_type, ip_addresses):
        count = 0
        for ip in ip_addresses:
            table_name = f"{system_type}_{ip.replace('.', '_')}"
            try:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE CHECK_RESULT = '취약'")
                    result = cursor.fetchone()
                    count += result[0] if result else 0
            except sqlite3.OperationalError:
                pass
            except Exception as e:
                print(f"Unexpected error: {e}")
        return count

    def fetch_severity_count_by_ip(self, checklist_table, system_type, ip_addresses, severity):
        count = 0
        for ip in ip_addresses:
            ip_table = f"{system_type}_{ip.replace('.', '_')}"
            try:
                with self.conn:
                    cursor = self.conn.cursor()
                    query = f"""
                    SELECT COUNT(*) FROM {checklist_table} c
                    JOIN {ip_table} i ON c.NO = i.NO
                    WHERE c.SEVERITY = ? AND i.CHECK_RESULT = '취약'
                    """
                    cursor.execute(query, (severity,))
                    result = cursor.fetchone()
                    count += result[0] if result else 0
            except sqlite3.OperationalError:
                pass
            except Exception as e:
                print(f"Unexpected error: {e}")
        return count

    def fetch_detail_data(self, system_type, ip_address):
        dynamic_table_name = f"{system_type}_{ip_address.replace('.', '_')}" if not system_type.endswith("_data") else system_type.replace("_data", "") + f"_{ip_address.replace('.', '_')}"
        checklist_table = f"{system_type}_checklist" if not system_type.endswith("_data") else system_type.replace("_data", "") + "_checklist"

        query = f"""
        SELECT c.NO, c.CATEGORY, c.CHECK_LIST, c.SEVERITY, d.CHECK_DETAIL, d.CHECK_RESULT
        FROM {checklist_table} c
        LEFT JOIN {dynamic_table_name} d ON c.NO = d.NO
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                return result
            else:
                return []
        except sqlite3.OperationalError as e:
            return []
        except Exception as e:
            return []

    def calculate_scores_for_all_ips(self, system_type, area_no):
        severity_weights = {'상': 3, '중': 2, '하': 1}
        scores = {'상': 0, '중': 0, '하': 0}

        completed_ips = self.fetch_completed_ips(f"{system_type}_data")

        for ip_row in completed_ips:
            ip_address = ip_row[0]
            ip_table_name = f"{system_type}_{ip_address.replace('.', '_')}"

            for severity in severity_weights.keys():
                query = f"""
                SELECT COUNT(*) FROM {system_type}_checklist c
                JOIN {ip_table_name} i ON c.NO = i.NO
                WHERE c.NO LIKE ? AND c.SEVERITY = ? AND i.CHECK_RESULT = '양호'
                """
                count = self.execute_query(query, (f"{area_no}_%", severity))
                scores[severity] += count * severity_weights[severity]

        return scores

    def calculate_max_scores(self, system_type):
        max_scores = {}
        severity_weights = {'상': 3, '중': 2, '하': 1}

        max_scores[system_type] = {}
        checklist_table = f"{system_type}_checklist"
        data_table = f"{system_type}_data"

        ip_count = self.get_data_count(data_table)

        checklist_data = self.fetch_all_data(checklist_table)

        for no, _, _, severity, _, _, _ in checklist_data:
            area_no = no.split('_')[0]
            if area_no not in max_scores[system_type]:
                max_scores[system_type][area_no] = 0

            max_scores[system_type][area_no] += severity_weights[severity] * ip_count

        return max_scores[system_type]

    def calculate_na_severity_scores(self, system_type):
        na_scores = {}

        completed_ips = self.fetch_completed_ips(f"{system_type}_data")

        checklist_data = self.fetch_all_data(f"{system_type}_checklist")
        area_nos = {data[0].split('_')[0] for data in checklist_data}

        for area_no in area_nos:
            na_scores[area_no] = 0

        for ip_row in completed_ips:
            ip_address = ip_row[0]
            ip_table_name = f"{system_type}_{ip_address.replace('.', '_')}"

            for area_no in area_nos:
                query = f"""
                SELECT c.SEVERITY, COUNT(*) FROM {system_type}_checklist c
                JOIN {ip_table_name} i ON c.NO = i.NO
                WHERE c.NO LIKE ? AND i.CHECK_RESULT = 'n/a'
                GROUP BY c.SEVERITY
                """
                cursor = self.conn.cursor()
                cursor.execute(query, (f"{area_no}_%",))
                results = cursor.fetchall()

                severity_weight = {'상': 3, '중': 2, '하': 1}
                for severity, count in results:
                    na_scores[area_no] += count * severity_weight.get(severity, 0)

        return na_scores

    def add_report_history(self, template, target, date, status):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO report_history (template, target, date, status)
            VALUES (?, ?, ?, ?);
        """, (template, target, date, status))
        self.conn.commit()

    def get_all_report_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM report_history;")
        result = cursor.fetchall()
        return result

    def delete_report_history(self, report_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM report_history WHERE id = ?;", (report_id,))
        self.conn.commit()

    def update_report_history(self, report_id, template, target, date, status):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE report_history
            SET template = ?, target = ?, date = ?, status = ?
            WHERE id = ?;
        """, (template, target, date, status, report_id))
        self.conn.commit()

    def search_inspection_results(self, system_type, ip=None, no=None, severity=None, result=None):
        try:
            cursor = self.conn.cursor()
            ip_query = f"SELECT IP_ADDRESS FROM {system_type}_data WHERE CHECK_DATE IS NOT NULL"
            ip_params = []
            if ip:
                ip_query += " AND IP_ADDRESS = ?"
                ip_params.append(ip)
            cursor.execute(ip_query, ip_params)
            ips = cursor.fetchall()

            results = []

            for ip_row in ips:
                ip_address = ip_row[0].replace('.', '_')
                dynamic_table_name = f"{system_type}_{ip_address}"
                detail_query = f"""
                SELECT '{system_type}' AS system_type, '{ip_row[0]}' AS IP_ADDRESS, c.NO, c.CATEGORY, c.CHECK_LIST, c.SEVERITY, r.CHECK_RESULT, r.CHECK_DETAIL
                FROM {system_type}_checklist c
                LEFT JOIN {dynamic_table_name} r ON c.NO = r.NO
                WHERE 1=1
                """

                query_params = []
                if no:
                    detail_query += " AND c.NO LIKE ?"
                    query_params.append(f"%{no}%")

                if severity:
                    detail_query += " AND c.SEVERITY = ?"
                    query_params.append(severity)

                if result:
                    detail_query += " AND r.CHECK_RESULT = ?"
                    query_params.append(result)

                cursor.execute(detail_query, query_params)
                results.extend(cursor.fetchall())

            return results

        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return []

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()[0]

    def close(self):
        if self.conn:
            self.conn.close()
