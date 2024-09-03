# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import os
import sys

# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class Functions:
    _icon_cache = {}
    _image_cache = {}

    @staticmethod
    def _get_base_path():
        # PyInstaller 실행 환경인 경우 _MEIPASS 경로 사용
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        # 개발 환경인 경우 현재 디렉토리 사용
        return os.path.abspath(os.getcwd())

    # SET SVG ICON WITH CACHING
    # ///////////////////////////////////////////////////////////////
    @staticmethod
    def set_svg_icon(icon_name):
        if icon_name in Functions._icon_cache:
            return Functions._icon_cache[icon_name]

        base_path = Functions._get_base_path()
        folder = "gui/images/svg_icons/"
        icon = os.path.normpath(os.path.join(base_path, folder, icon_name))
        Functions._icon_cache[icon_name] = icon
        return icon
    
    # SET SVG IMAGE WITH CACHING
    # ///////////////////////////////////////////////////////////////
    @staticmethod
    def set_svg_image(icon_name):
        if icon_name in Functions._image_cache:
            return Functions._image_cache[icon_name]

        base_path = Functions._get_base_path()
        folder = "gui/images/svg_images/"
        image = os.path.normpath(os.path.join(base_path, folder, icon_name))
        Functions._image_cache[icon_name] = image
        return image

    # SET IMAGE WITH CACHING
    # ///////////////////////////////////////////////////////////////
    @staticmethod
    def set_image(image_name):
        if image_name in Functions._image_cache:
            return Functions._image_cache[image_name]

        base_path = Functions._get_base_path()
        folder = "gui/images/images/"
        image = os.path.normpath(os.path.join(base_path, folder, image_name))
        Functions._image_cache[image_name] = image
        return image
