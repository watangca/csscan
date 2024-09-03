# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import json
import os

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
import sys
from gui.core.json_settings import Settings

# APP THEMES
# ///////////////////////////////////////////////////////////////
class Themes(object):
    # LOAD SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Themes, self).__init__()

        # Settings 객체 초기화
        self.setup_settings = Settings()
        self._settings = self.setup_settings.items

        # PyInstaller 실행 환경인 경우, _MEIPASS 경로 사용
        if getattr(sys, 'frozen', False):
            self.app_path = sys._MEIPASS
        # 개발 환경인 경우, 현재 작업 디렉토리 사용
        else:
            self.app_path = os.path.abspath(os.getcwd())

        self.json_file = f"gui/themes/{self._settings['theme_name']}.json"
        self.settings_path = os.path.normpath(os.path.join(self.app_path, self.json_file))

        if not os.path.isfile(self.settings_path):
            print(f"WARNING: \"{self.json_file}\" not found! check in the folder {self.settings_path}")

        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        # READ JSON FILE
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings