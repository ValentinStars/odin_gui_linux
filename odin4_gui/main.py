import json
import os
import shlex
import shutil
import signal
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from PySide6 import QtCore, QtGui, QtWidgets

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
THEME_PATH = BUNDLE_DIR / "theme.qss"
DEFAULT_PROFILES_PATH = BUNDLE_DIR / "profiles" / "devices.json"


def _config_dir() -> Path:
    base = Path(
        QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
    )
    base.mkdir(parents=True, exist_ok=True)
    return base


def _profiles_path() -> Path:
    config_dir = _config_dir()
    user_profiles = config_dir / "devices.json"
    if not user_profiles.exists() and DEFAULT_PROFILES_PATH.exists():
        try:
            shutil.copy(DEFAULT_PROFILES_PATH, user_profiles)
        except OSError:
            return DEFAULT_PROFILES_PATH
    return user_profiles if user_profiles.exists() else DEFAULT_PROFILES_PATH


def _settings_path() -> Path:
    return _config_dir() / "settings.json"


def _default_odin_path() -> str:
    bundle_odin = BUNDLE_DIR / "odin4"
    if bundle_odin.exists():
        return str(bundle_odin)
    root_odin = ROOT_DIR / "odin4"
    if root_odin.exists():
        return str(root_odin)
    return ""


def _default_adb_path() -> str:
    bundle_adb = BUNDLE_DIR / "adb"
    if bundle_adb.exists():
        return str(bundle_adb)
    system_adb = shutil.which("adb")
    return system_adb or ""


def _default_language() -> str:
    return "ru" if QtCore.QLocale.system().language() == QtCore.QLocale.Russian else "en"


FILE_KEYS = ["BL", "AP", "CP", "CSC", "UMS"]

STRINGS = {
    "en": {
        "app_title": "odin",
        "brand": "odin",
        "sub_brand": "Odin4 wrapper + tools",
        "author": "Valentin Stars",
        "nav_flash": "Flash",
        "nav_adb": "ADB",
        "nav_profiles": "Profiles",
        "nav_logs": "Logs",
        "nav_settings": "Settings",
        "status_idle": "Idle",
        "status_flashing": "Flashing...",
        "device_not_checked": "Device: not checked",
        "device_not_found": "Device: not found",
        "device_found": "Device: {count} found",
        "group_odin": "Odin4 Binary",
        "group_firmware": "Firmware Files",
        "group_auto_detect": "Auto-detect Firmware Folder",
        "group_device": "Target Device",
        "group_options": "Options",
        "group_actions": "Safety and Actions",
        "group_adb": "ADB Binary",
        "group_adb_devices": "ADB Devices",
        "group_quick_actions": "Quick Actions",
        "group_file_ops": "File Operations",
        "group_adb_shell": "ADB Shell",
        "group_profiles": "Device Profiles",
        "group_logs": "Logs",
        "group_settings": "App Settings",
        "ph_odin_path": "Path to odin4",
        "ph_select_file": "Select {key} file",
        "ph_fw_folder": "Folder with BL/AP/CP/CSC files",
        "ph_device_path": "Manual device path (optional)",
        "ph_command_preview": "Command preview",
        "ph_adb_path": "Path to adb",
        "ph_adb_push_local": "Local file to push",
        "ph_adb_pull_remote": "Remote path to pull",
        "ph_adb_pull_local": "Local folder",
        "ph_adb_install_apk": "APK to install",
        "ph_adb_shell_cmd": "getprop ro.product.model",
        "btn_browse": "Browse",
        "btn_auto_detect": "Auto-detect",
        "btn_clear": "Clear",
        "btn_scan": "Scan",
        "btn_refresh": "Refresh",
        "btn_copy": "Copy",
        "btn_flash": "Flash",
        "btn_stop": "Stop",
        "chk_prefer_home_csc": "Prefer HOME_CSC",
        "chk_nand_erase": "Nand erase (-e)",
        "chk_home_validate": "Home validation (-V)",
        "chk_reboot": "Reboot (--reboot)",
        "chk_redownload": "Redownload (--redownload)",
        "chk_confirm_risk": "I understand the risks",
        "chk_confirm_download": "Device is in Download Mode",
        "combo_auto_device": "Auto-detect (no -d)",
        "combo_all_devices": "All devices",
        "combo_no_profile": "No profile",
        "btn_reboot_download": "Reboot to Download",
        "btn_reboot_recovery": "Reboot to Recovery",
        "btn_reboot_system": "Reboot System",
        "btn_kill_adb": "Kill ADB Server",
        "btn_start_adb": "Start ADB Server",
        "btn_push": "Push",
        "btn_pull": "Pull",
        "btn_install_apk": "Install APK",
        "btn_run": "Run",
        "btn_load_folder": "Load Firmware Folder",
        "btn_apply_profile": "Apply to Flash",
        "btn_flash_stock": "Flash Stock",
        "btn_open_profiles": "Open profiles file",
        "btn_save_log": "Save Log",
        "btn_clear_log": "Clear",
        "chk_autoscroll": "Auto-scroll logs",
        "chk_timestamp": "Timestamps in logs",
        "lbl_theme": "Theme",
        "lbl_language": "Language",
        "theme_custom": "Odin VST",
        "theme_qt": "Qt Default",
        "lang_ru": "Russian",
        "lang_en": "English",
        "no_devices": "No devices",
        "profile_none": "No profile selected",
        "profile_name": "Name",
        "profile_model": "Model",
        "profile_notes": "Notes",
        "profile_patterns": "Patterns",
        "profile_flags": "Flags",
        "dlg_confirm_title": "Confirm Flash",
        "dlg_confirm_text": "Flashing can brick devices. Continue?",
        "dlg_select_odin": "Select odin4",
        "dlg_select_adb": "Select adb",
        "dlg_select_file": "Select {key} file",
        "dlg_select_folder": "Select firmware folder",
        "dlg_select_push": "Select file to push",
        "dlg_select_pull_folder": "Select local folder",
        "dlg_select_apk": "Select APK",
        "dlg_save_log": "Save log",
    },
    "ru": {
        "app_title": "odin",
        "brand": "odin",
        "sub_brand": "Оболочка Odin4 + инструменты",
        "author": "Valentin Stars",
        "nav_flash": "Прошивка",
        "nav_adb": "ADB",
        "nav_profiles": "Профили",
        "nav_logs": "Логи",
        "nav_settings": "Настройки",
        "status_idle": "Ожидание",
        "status_flashing": "Прошивка...",
        "device_not_checked": "Устройство: не проверено",
        "device_not_found": "Устройство: не найдено",
        "device_found": "Устройств найдено: {count}",
        "group_odin": "Файл Odin4",
        "group_firmware": "Файлы прошивки",
        "group_auto_detect": "Автопоиск папки прошивки",
        "group_device": "Устройство",
        "group_options": "Опции",
        "group_actions": "Безопасность и действия",
        "group_adb": "Файл ADB",
        "group_adb_devices": "ADB устройства",
        "group_quick_actions": "Быстрые действия",
        "group_file_ops": "Файловые операции",
        "group_adb_shell": "ADB Shell",
        "group_profiles": "Профили устройств",
        "group_logs": "Логи",
        "group_settings": "Настройки приложения",
        "ph_odin_path": "Путь к odin4",
        "ph_select_file": "Выбрать файл {key}",
        "ph_fw_folder": "Папка с BL/AP/CP/CSC файлами",
        "ph_device_path": "Путь к устройству (опционально)",
        "ph_command_preview": "Предпросмотр команды",
        "ph_adb_path": "Путь к adb",
        "ph_adb_push_local": "Локальный файл для push",
        "ph_adb_pull_remote": "Удаленный путь для pull",
        "ph_adb_pull_local": "Локальная папка",
        "ph_adb_install_apk": "APK для установки",
        "ph_adb_shell_cmd": "getprop ro.product.model",
        "btn_browse": "Обзор",
        "btn_auto_detect": "Авто-поиск",
        "btn_clear": "Очистить",
        "btn_scan": "Сканировать",
        "btn_refresh": "Обновить",
        "btn_copy": "Копировать",
        "btn_flash": "Прошить",
        "btn_stop": "Стоп",
        "chk_prefer_home_csc": "Предпочитать HOME_CSC",
        "chk_nand_erase": "Стереть NAND (-e)",
        "chk_home_validate": "Проверка HOME (-V)",
        "chk_reboot": "Перезагрузка (--reboot)",
        "chk_redownload": "Перезаход в Download (--redownload)",
        "chk_confirm_risk": "Я понимаю риски",
        "chk_confirm_download": "Устройство в Download Mode",
        "combo_auto_device": "Авто-определение (без -d)",
        "combo_all_devices": "Все устройства",
        "combo_no_profile": "Без профиля",
        "btn_reboot_download": "Ребут в Download",
        "btn_reboot_recovery": "Ребут в Recovery",
        "btn_reboot_system": "Ребут системы",
        "btn_kill_adb": "Остановить ADB",
        "btn_start_adb": "Запустить ADB",
        "btn_push": "Push",
        "btn_pull": "Pull",
        "btn_install_apk": "Установить APK",
        "btn_run": "Выполнить",
        "btn_load_folder": "Загрузить папку прошивки",
        "btn_apply_profile": "Применить к прошивке",
        "btn_flash_stock": "Прошить сток",
        "btn_open_profiles": "Открыть файл профилей",
        "btn_save_log": "Сохранить лог",
        "btn_clear_log": "Очистить",
        "chk_autoscroll": "Автопрокрутка логов",
        "chk_timestamp": "Временные метки в логах",
        "lbl_theme": "Тема",
        "lbl_language": "Язык",
        "theme_custom": "Odin VST",
        "theme_qt": "Стандартная Qt",
        "lang_ru": "Русский",
        "lang_en": "Английский",
        "no_devices": "Устройств нет",
        "profile_none": "Профиль не выбран",
        "profile_name": "Имя",
        "profile_model": "Модель",
        "profile_notes": "Заметки",
        "profile_patterns": "Шаблоны",
        "profile_flags": "Флаги",
        "dlg_confirm_title": "Подтверждение прошивки",
        "dlg_confirm_text": "Прошивка может повредить устройство. Продолжить?",
        "dlg_select_odin": "Выберите odin4",
        "dlg_select_adb": "Выберите adb",
        "dlg_select_file": "Выберите файл {key}",
        "dlg_select_folder": "Выберите папку прошивки",
        "dlg_select_push": "Выберите файл для push",
        "dlg_select_pull_folder": "Выберите локальную папку",
        "dlg_select_apk": "Выберите APK",
        "dlg_save_log": "Сохранить лог",
    },
}


@dataclass
class Profile:
    profile_id: str
    name: str
    model: str
    notes: str
    patterns: Dict[str, str]
    flags: Dict[str, bool]
    default_csc_prefer_home: bool


def load_profiles() -> List[Profile]:
    profiles_path = _profiles_path()
    if not profiles_path.exists():
        return []
    try:
        with profiles_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        profiles = []
        for item in data.get("profiles", []):
            profiles.append(
                Profile(
                    profile_id=item.get("id", ""),
                    name=item.get("name", "Unnamed"),
                    model=item.get("model", ""),
                    notes=item.get("notes", ""),
                    patterns=item.get("patterns", {}),
                    flags=item.get("flags", {}),
                    default_csc_prefer_home=bool(item.get("default_csc_prefer_home", True)),
                )
            )
        return profiles
    except (OSError, json.JSONDecodeError):
        return []


def load_settings() -> Dict:
    settings_path = _settings_path()
    if not settings_path.exists():
        return {}
    try:
        with settings_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def save_settings(settings: Dict) -> None:
    settings_path = _settings_path()
    try:
        with settings_path.open("w", encoding="utf-8") as handle:
            json.dump(settings, handle, indent=2)
    except OSError:
        pass


def find_first_match(folder: Path, pattern: str) -> Optional[Path]:
    matches = sorted(folder.glob(pattern))
    return matches[0] if matches else None


def detect_firmware(folder: Path, patterns: Dict[str, str], prefer_home_csc: bool) -> Dict[str, Optional[Path]]:
    result: Dict[str, Optional[Path]] = {key: None for key in FILE_KEYS}
    bl = find_first_match(folder, patterns.get("BL", "")) if patterns.get("BL") else None
    ap = find_first_match(folder, patterns.get("AP", "")) if patterns.get("AP") else None
    cp = find_first_match(folder, patterns.get("CP", "")) if patterns.get("CP") else None
    csc = find_first_match(folder, patterns.get("CSC", "")) if patterns.get("CSC") else None
    home_csc = find_first_match(folder, patterns.get("HOME_CSC", "")) if patterns.get("HOME_CSC") else None

    result["BL"] = bl
    result["AP"] = ap
    result["CP"] = cp
    if prefer_home_csc and home_csc is not None:
        result["CSC"] = home_csc
    else:
        result["CSC"] = csc
    return result


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("odin")
        self.resize(1180, 720)

        self.settings = load_settings()
        self.profiles = load_profiles()
        self.profile_files: Dict[str, Path] = {}

        self.current_language = self.settings.get("language", _default_language())
        self.current_theme = self.settings.get("theme", "custom")
        self.current_status_key = "idle"
        self.last_device_count: Optional[int] = None

        self.flash_process: Optional[QtCore.QProcess] = None
        self.other_processes: List[QtCore.QProcess] = []
        self.log_lines: List[str] = []

        self._build_ui()
        self._apply_settings()
        self._apply_theme()
        self._apply_language()
        self._refresh_command_preview()
        self._update_flash_ready()

    def _apply_theme(self) -> None:
        theme = self.theme_combo.currentData() if hasattr(self, "theme_combo") else None
        if theme:
            self.current_theme = theme
        if self.current_theme == "qt":
            self.setStyleSheet("")
            return
        if THEME_PATH.exists():
            with THEME_PATH.open("r", encoding="utf-8") as handle:
                self.setStyleSheet(handle.read())

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        root_layout = QtWidgets.QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QtWidgets.QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 18, 18, 18)
        sidebar_layout.setSpacing(12)

        self.brand_label = QtWidgets.QLabel()
        self.brand_label.setObjectName("BrandLabel")
        self.sub_brand_label = QtWidgets.QLabel()
        self.sub_brand_label.setObjectName("SubBrandLabel")
        sidebar_layout.addWidget(self.brand_label)
        sidebar_layout.addWidget(self.sub_brand_label)

        self.nav_group = QtWidgets.QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.nav_buttons: Dict[str, QtWidgets.QToolButton] = {}
        for key in ["flash", "adb", "profiles", "logs", "settings"]:
            btn = QtWidgets.QToolButton()
            btn.setCheckable(True)
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
            self.nav_group.addButton(btn)
            self.nav_buttons[key] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch(1)

        status_card = QtWidgets.QFrame()
        status_card.setObjectName("Card")
        status_layout = QtWidgets.QVBoxLayout(status_card)
        status_layout.setContentsMargins(12, 12, 12, 12)
        status_layout.setSpacing(6)
        self.status_label = QtWidgets.QLabel()
        self.status_label.setObjectName("AccentLabel")
        self.device_status_label = QtWidgets.QLabel()
        self.device_status_label.setObjectName("MutedLabel")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.device_status_label)
        sidebar_layout.addWidget(status_card)

        self.author_label = QtWidgets.QLabel()
        self.author_label.setObjectName("MutedLabel")
        self.author_label.setTextFormat(QtCore.Qt.RichText)
        self.author_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.author_label.setOpenExternalLinks(True)
        sidebar_layout.addWidget(self.author_label)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = {
            "flash": self._wrap_scroll(self._build_flash_page()),
            "adb": self._wrap_scroll(self._build_adb_page()),
            "profiles": self._wrap_scroll(self._build_profiles_page()),
            "logs": self._wrap_scroll(self._build_logs_page()),
            "settings": self._wrap_scroll(self._build_settings_page()),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        root_layout.addWidget(sidebar, 0)
        root_layout.addWidget(self.stack, 1)

        self.setCentralWidget(central)

        self.nav_buttons["flash"].setChecked(True)
        self.stack.setCurrentWidget(self.pages["flash"])
        self.nav_group.buttonClicked.connect(self._switch_page)

    def _wrap_scroll(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setWidget(widget)
        return scroll

    def _t(self, msg_key: str, **kwargs) -> str:
        lang = self.current_language if self.current_language in STRINGS else "en"
        value = STRINGS.get(lang, {}).get(msg_key) or STRINGS["en"].get(msg_key) or msg_key
        try:
            return value.format(**kwargs)
        except (KeyError, ValueError):
            return value

    def _apply_language(self) -> None:
        if hasattr(self, "lang_combo") and self.lang_combo.currentData():
            self.current_language = self.lang_combo.currentData()

        self.setWindowTitle(self._t("app_title"))
        self.brand_label.setText(self._t("brand"))
        self.sub_brand_label.setText(self._t("sub_brand"))
        self.author_label.setText(
            f'<a href="https://vstbio.t.me">{self._t("author")}</a>'
        )

        self.nav_buttons["flash"].setText(self._t("nav_flash"))
        self.nav_buttons["adb"].setText(self._t("nav_adb"))
        self.nav_buttons["profiles"].setText(self._t("nav_profiles"))
        self.nav_buttons["logs"].setText(self._t("nav_logs"))
        self.nav_buttons["settings"].setText(self._t("nav_settings"))

        self._set_status(self.current_status_key)
        self._set_device_status(self.last_device_count)

        self.odin_group.setTitle(self._t("group_odin"))
        self.files_group.setTitle(self._t("group_firmware"))
        self.detect_group.setTitle(self._t("group_auto_detect"))
        self.device_group.setTitle(self._t("group_device"))
        self.options_group.setTitle(self._t("group_options"))
        self.action_group.setTitle(self._t("group_actions"))

        self.odin_path_edit.setPlaceholderText(self._t("ph_odin_path"))
        for key, edit in self.file_edits.items():
            edit.setPlaceholderText(self._t("ph_select_file", key=key))
        self.firmware_folder_edit.setPlaceholderText(self._t("ph_fw_folder"))
        self.device_path_edit.setPlaceholderText(self._t("ph_device_path"))
        self.command_preview.setPlaceholderText(self._t("ph_command_preview"))

        self.prefer_home_csc.setText(self._t("chk_prefer_home_csc"))
        self.opt_nand_erase.setText(self._t("chk_nand_erase"))
        self.opt_home_validate.setText(self._t("chk_home_validate"))
        self.opt_reboot.setText(self._t("chk_reboot"))
        self.opt_redownload.setText(self._t("chk_redownload"))
        self.confirm_risk.setText(self._t("chk_confirm_risk"))
        self.confirm_download.setText(self._t("chk_confirm_download"))

        self.copy_cmd.setText(self._t("btn_copy"))
        self.flash_button.setText(self._t("btn_flash"))
        self.stop_button.setText(self._t("btn_stop"))
        self.refresh_devices.setText(self._t("btn_refresh"))
        self.browse_odin.setText(self._t("btn_browse"))
        self.detect_odin.setText(self._t("btn_auto_detect"))
        self.browse_folder.setText(self._t("btn_browse"))
        self.scan_folder.setText(self._t("btn_scan"))

        for key in FILE_KEYS:
            self.file_browse_buttons[key].setText(self._t("btn_browse"))
            self.file_clear_buttons[key].setText(self._t("btn_clear"))

        if self.device_combo.count() > 0:
            self.device_combo.setItemText(0, self._t("combo_auto_device"))

        self.adb_group.setTitle(self._t("group_adb"))
        self.adb_devices_group.setTitle(self._t("group_adb_devices"))
        self.adb_actions_group.setTitle(self._t("group_quick_actions"))
        self.adb_file_group.setTitle(self._t("group_file_ops"))
        self.adb_shell_group.setTitle(self._t("group_adb_shell"))

        self.adb_path_edit.setPlaceholderText(self._t("ph_adb_path"))
        self.adb_push_local.setPlaceholderText(self._t("ph_adb_push_local"))
        self.adb_pull_remote.setPlaceholderText(self._t("ph_adb_pull_remote"))
        self.adb_pull_local.setPlaceholderText(self._t("ph_adb_pull_local"))
        self.adb_install_apk.setPlaceholderText(self._t("ph_adb_install_apk"))
        self.adb_shell_cmd.setPlaceholderText(self._t("ph_adb_shell_cmd"))

        self.browse_adb.setText(self._t("btn_browse"))
        self.detect_adb.setText(self._t("btn_auto_detect"))
        self.refresh_adb.setText(self._t("btn_refresh"))
        self.reboot_download.setText(self._t("btn_reboot_download"))
        self.reboot_recovery.setText(self._t("btn_reboot_recovery"))
        self.reboot_system.setText(self._t("btn_reboot_system"))
        self.kill_server.setText(self._t("btn_kill_adb"))
        self.start_server.setText(self._t("btn_start_adb"))
        self.push_btn.setText(self._t("btn_push"))
        self.pull_btn.setText(self._t("btn_pull"))
        self.install_btn.setText(self._t("btn_install_apk"))
        self.shell_run.setText(self._t("btn_run"))
        self.push_browse.setText(self._t("btn_browse"))
        self.pull_browse.setText(self._t("btn_browse"))
        self.install_browse.setText(self._t("btn_browse"))

        if self.adb_device_combo.count() > 0:
            self.adb_device_combo.setItemText(0, self._t("combo_all_devices"))
        if self.adb_devices_view.toPlainText().strip() == STRINGS["en"]["no_devices"] or \
                self.adb_devices_view.toPlainText().strip() == STRINGS["ru"]["no_devices"]:
            self.adb_devices_view.setPlainText(self._t("no_devices"))

        self.profile_group.setTitle(self._t("group_profiles"))
        self.load_folder.setText(self._t("btn_load_folder"))
        self.apply_profile.setText(self._t("btn_apply_profile"))
        self.flash_profile.setText(self._t("btn_flash_stock"))
        self.open_profiles.setText(self._t("btn_open_profiles"))
        if self.profile_combo.count() > 0:
            self.profile_combo.setItemText(0, self._t("combo_no_profile"))

        if self._current_profile() is None:
            self.profile_details.setPlainText(self._t("profile_none"))
        else:
            self._profile_changed()

        self.log_group.setTitle(self._t("group_logs"))
        self.save_log.setText(self._t("btn_save_log"))
        self.clear_log.setText(self._t("btn_clear_log"))

        self.settings_group.setTitle(self._t("group_settings"))
        self.setting_autoscroll.setText(self._t("chk_autoscroll"))
        self.setting_timestamp.setText(self._t("chk_timestamp"))
        self.theme_label.setText(self._t("lbl_theme"))
        self.lang_label.setText(self._t("lbl_language"))
        if self.theme_combo.count() >= 2:
            self.theme_combo.setItemText(0, self._t("theme_custom"))
            self.theme_combo.setItemText(1, self._t("theme_qt"))
        if self.lang_combo.count() >= 2:
            self.lang_combo.setItemText(0, self._t("lang_ru"))
            self.lang_combo.setItemText(1, self._t("lang_en"))

    def _set_status(self, key: str) -> None:
        self.current_status_key = key
        self.status_label.setText(self._t(f"status_{key}"))

    def _set_device_status(self, count: Optional[int]) -> None:
        self.last_device_count = count
        if count is None:
            self.device_status_label.setText(self._t("device_not_checked"))
        elif count <= 0:
            self.device_status_label.setText(self._t("device_not_found"))
        else:
            self.device_status_label.setText(self._t("device_found", count=count))

    def _switch_page(self, button: QtWidgets.QAbstractButton) -> None:
        for key, btn in self.nav_buttons.items():
            if btn is button:
                self.stack.setCurrentWidget(self.pages[key])
                break

    def _build_flash_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.odin_group = QtWidgets.QGroupBox()
        odin_layout = QtWidgets.QHBoxLayout(self.odin_group)
        self.odin_path_edit = QtWidgets.QLineEdit()
        self.odin_path_edit.textChanged.connect(self._refresh_command_preview)
        self.odin_path_edit.textChanged.connect(self._update_flash_ready)
        self.browse_odin = QtWidgets.QPushButton()
        self.browse_odin.clicked.connect(self._select_odin_path)
        self.detect_odin = QtWidgets.QPushButton()
        self.detect_odin.clicked.connect(self._auto_detect_odin)
        odin_layout.addWidget(self.odin_path_edit, 1)
        odin_layout.addWidget(self.browse_odin)
        odin_layout.addWidget(self.detect_odin)

        self.files_group = QtWidgets.QGroupBox()
        files_layout = QtWidgets.QGridLayout(self.files_group)
        files_layout.setHorizontalSpacing(10)
        files_layout.setVerticalSpacing(10)

        self.file_edits: Dict[str, QtWidgets.QLineEdit] = {}
        self.file_browse_buttons: Dict[str, QtWidgets.QPushButton] = {}
        self.file_clear_buttons: Dict[str, QtWidgets.QPushButton] = {}
        row = 0
        for key in FILE_KEYS:
            label = QtWidgets.QLabel(key)
            edit = QtWidgets.QLineEdit()
            edit.textChanged.connect(self._refresh_command_preview)
            edit.textChanged.connect(self._update_flash_ready)
            browse = QtWidgets.QPushButton()
            browse.clicked.connect(lambda _checked=False, k=key: self._select_file(k))
            clear = QtWidgets.QPushButton()
            clear.clicked.connect(lambda _checked=False, k=key: self._clear_file(k))
            files_layout.addWidget(label, row, 0)
            files_layout.addWidget(edit, row, 1)
            files_layout.addWidget(browse, row, 2)
            files_layout.addWidget(clear, row, 3)
            self.file_edits[key] = edit
            self.file_browse_buttons[key] = browse
            self.file_clear_buttons[key] = clear
            row += 1

        self.detect_group = QtWidgets.QGroupBox()
        detect_layout = QtWidgets.QGridLayout(self.detect_group)
        self.firmware_folder_edit = QtWidgets.QLineEdit()
        self.browse_folder = QtWidgets.QPushButton()
        self.browse_folder.clicked.connect(self._select_firmware_folder)
        self.scan_folder = QtWidgets.QPushButton()
        self.scan_folder.clicked.connect(self._scan_firmware_folder)
        self.prefer_home_csc = QtWidgets.QCheckBox()
        self.prefer_home_csc.stateChanged.connect(self._update_flash_ready)
        detect_layout.addWidget(self.firmware_folder_edit, 0, 0, 1, 2)
        detect_layout.addWidget(self.browse_folder, 0, 2)
        detect_layout.addWidget(self.scan_folder, 0, 3)
        detect_layout.addWidget(self.prefer_home_csc, 1, 0, 1, 2)

        self.device_group = QtWidgets.QGroupBox()
        device_layout = QtWidgets.QGridLayout(self.device_group)
        self.device_combo = QtWidgets.QComboBox()
        self.device_combo.addItem("")
        self.device_combo.currentIndexChanged.connect(self._refresh_command_preview)
        self.refresh_devices = QtWidgets.QPushButton()
        self.refresh_devices.clicked.connect(self._refresh_odin_devices)
        self.device_path_edit = QtWidgets.QLineEdit()
        self.device_path_edit.textChanged.connect(self._refresh_command_preview)
        device_layout.addWidget(self.device_combo, 0, 0)
        device_layout.addWidget(self.refresh_devices, 0, 1)
        device_layout.addWidget(self.device_path_edit, 1, 0, 1, 2)

        self.options_group = QtWidgets.QGroupBox()
        options_layout = QtWidgets.QGridLayout(self.options_group)
        self.opt_nand_erase = QtWidgets.QCheckBox()
        self.opt_home_validate = QtWidgets.QCheckBox()
        self.opt_reboot = QtWidgets.QCheckBox()
        self.opt_redownload = QtWidgets.QCheckBox()
        for checkbox in [
            self.opt_nand_erase,
            self.opt_home_validate,
            self.opt_reboot,
            self.opt_redownload,
        ]:
            checkbox.stateChanged.connect(self._refresh_command_preview)
        options_layout.addWidget(self.opt_nand_erase, 0, 0)
        options_layout.addWidget(self.opt_home_validate, 0, 1)
        options_layout.addWidget(self.opt_reboot, 1, 0)
        options_layout.addWidget(self.opt_redownload, 1, 1)

        self.action_group = QtWidgets.QGroupBox()
        action_layout = QtWidgets.QGridLayout(self.action_group)
        self.confirm_risk = QtWidgets.QCheckBox()
        self.confirm_download = QtWidgets.QCheckBox()
        self.confirm_risk.stateChanged.connect(self._update_flash_ready)
        self.confirm_download.stateChanged.connect(self._update_flash_ready)
        self.command_preview = QtWidgets.QLineEdit()
        self.command_preview.setReadOnly(True)
        self.copy_cmd = QtWidgets.QPushButton()
        self.copy_cmd.clicked.connect(self._copy_command)
        self.flash_button = QtWidgets.QPushButton()
        self.flash_button.setObjectName("PrimaryButton")
        self.flash_button.clicked.connect(self._start_flash)
        self.stop_button = QtWidgets.QPushButton()
        self.stop_button.setObjectName("DangerButton")
        self.stop_button.clicked.connect(self._stop_flash)
        self.stop_button.setEnabled(False)

        action_layout.addWidget(self.confirm_risk, 0, 0)
        action_layout.addWidget(self.confirm_download, 0, 1)
        action_layout.addWidget(self.command_preview, 1, 0, 1, 2)
        action_layout.addWidget(self.copy_cmd, 1, 2)
        action_layout.addWidget(self.flash_button, 2, 0)
        action_layout.addWidget(self.stop_button, 2, 1)

        self.flash_progress = QtWidgets.QProgressBar()
        self.flash_progress.setRange(0, 1)
        self.flash_progress.setValue(0)

        layout.addWidget(self.odin_group)
        layout.addWidget(self.files_group)
        layout.addWidget(self.detect_group)
        layout.addWidget(self.device_group)
        layout.addWidget(self.options_group)
        layout.addWidget(self.action_group)
        layout.addWidget(self.flash_progress)
        layout.addStretch(1)

        return page

    def _build_adb_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.adb_group = QtWidgets.QGroupBox()
        adb_layout = QtWidgets.QHBoxLayout(self.adb_group)
        self.adb_path_edit = QtWidgets.QLineEdit()
        self.browse_adb = QtWidgets.QPushButton()
        self.browse_adb.clicked.connect(self._select_adb_path)
        self.detect_adb = QtWidgets.QPushButton()
        self.detect_adb.clicked.connect(self._auto_detect_adb)
        adb_layout.addWidget(self.adb_path_edit, 1)
        adb_layout.addWidget(self.browse_adb)
        adb_layout.addWidget(self.detect_adb)

        self.adb_devices_group = QtWidgets.QGroupBox()
        device_layout = QtWidgets.QGridLayout(self.adb_devices_group)
        self.adb_device_combo = QtWidgets.QComboBox()
        self.adb_device_combo.addItem("")
        self.refresh_adb = QtWidgets.QPushButton()
        self.refresh_adb.clicked.connect(self._refresh_adb_devices)
        self.adb_devices_view = QtWidgets.QPlainTextEdit()
        self.adb_devices_view.setReadOnly(True)
        device_layout.addWidget(self.adb_device_combo, 0, 0)
        device_layout.addWidget(self.refresh_adb, 0, 1)
        device_layout.addWidget(self.adb_devices_view, 1, 0, 1, 2)

        self.adb_actions_group = QtWidgets.QGroupBox()
        actions_layout = QtWidgets.QGridLayout(self.adb_actions_group)
        self.reboot_download = QtWidgets.QPushButton()
        self.reboot_recovery = QtWidgets.QPushButton()
        self.reboot_system = QtWidgets.QPushButton()
        self.kill_server = QtWidgets.QPushButton()
        self.start_server = QtWidgets.QPushButton()
        self.reboot_download.clicked.connect(lambda: self._adb_command(["reboot", "download"]))
        self.reboot_recovery.clicked.connect(lambda: self._adb_command(["reboot", "recovery"]))
        self.reboot_system.clicked.connect(lambda: self._adb_command(["reboot"]))
        self.kill_server.clicked.connect(lambda: self._adb_command(["kill-server"]))
        self.start_server.clicked.connect(lambda: self._adb_command(["start-server"]))
        actions_layout.addWidget(self.reboot_download, 0, 0)
        actions_layout.addWidget(self.reboot_recovery, 0, 1)
        actions_layout.addWidget(self.reboot_system, 0, 2)
        actions_layout.addWidget(self.kill_server, 1, 0)
        actions_layout.addWidget(self.start_server, 1, 1)

        self.adb_file_group = QtWidgets.QGroupBox()
        file_layout = QtWidgets.QGridLayout(self.adb_file_group)
        self.adb_push_local = QtWidgets.QLineEdit()
        self.push_browse = QtWidgets.QPushButton()
        self.push_browse.clicked.connect(self._select_adb_push_file)
        self.adb_push_remote = QtWidgets.QLineEdit("/sdcard/Download/")
        self.push_btn = QtWidgets.QPushButton()
        self.push_btn.clicked.connect(self._adb_push)

        self.adb_pull_remote = QtWidgets.QLineEdit()
        self.adb_pull_local = QtWidgets.QLineEdit()
        self.pull_browse = QtWidgets.QPushButton()
        self.pull_browse.clicked.connect(self._select_adb_pull_folder)
        self.pull_btn = QtWidgets.QPushButton()
        self.pull_btn.clicked.connect(self._adb_pull)

        self.adb_install_apk = QtWidgets.QLineEdit()
        self.install_browse = QtWidgets.QPushButton()
        self.install_browse.clicked.connect(self._select_adb_install_apk)
        self.install_btn = QtWidgets.QPushButton()
        self.install_btn.clicked.connect(self._adb_install)

        file_layout.addWidget(self.adb_push_local, 0, 0)
        file_layout.addWidget(self.push_browse, 0, 1)
        file_layout.addWidget(self.adb_push_remote, 0, 2)
        file_layout.addWidget(self.push_btn, 0, 3)

        file_layout.addWidget(self.adb_pull_remote, 1, 0)
        file_layout.addWidget(self.adb_pull_local, 1, 1)
        file_layout.addWidget(self.pull_browse, 1, 2)
        file_layout.addWidget(self.pull_btn, 1, 3)

        file_layout.addWidget(self.adb_install_apk, 2, 0)
        file_layout.addWidget(self.install_browse, 2, 1)
        file_layout.addWidget(self.install_btn, 2, 2)

        self.adb_shell_group = QtWidgets.QGroupBox()
        shell_layout = QtWidgets.QHBoxLayout(self.adb_shell_group)
        self.adb_shell_cmd = QtWidgets.QLineEdit()
        self.shell_run = QtWidgets.QPushButton()
        self.shell_run.clicked.connect(self._adb_shell)
        shell_layout.addWidget(self.adb_shell_cmd, 1)
        shell_layout.addWidget(self.shell_run)

        layout.addWidget(self.adb_group)
        layout.addWidget(self.adb_devices_group)
        layout.addWidget(self.adb_actions_group)
        layout.addWidget(self.adb_file_group)
        layout.addWidget(self.adb_shell_group)
        layout.addStretch(1)

        return page

    def _build_profiles_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.profile_group = QtWidgets.QGroupBox()
        profile_layout = QtWidgets.QGridLayout(self.profile_group)
        self.profile_combo = QtWidgets.QComboBox()
        self.profile_combo.addItem("")
        for profile in self.profiles:
            self.profile_combo.addItem(profile.name, profile.profile_id)
        self.profile_combo.currentIndexChanged.connect(self._profile_changed)
        self.profile_details = QtWidgets.QPlainTextEdit()
        self.profile_details.setReadOnly(True)
        self.load_folder = QtWidgets.QPushButton()
        self.load_folder.clicked.connect(self._profile_load_folder)
        self.apply_profile = QtWidgets.QPushButton()
        self.apply_profile.clicked.connect(self._profile_apply)
        self.flash_profile = QtWidgets.QPushButton()
        self.flash_profile.setObjectName("PrimaryButton")
        self.flash_profile.clicked.connect(self._profile_flash)
        self.open_profiles = QtWidgets.QPushButton()
        self.open_profiles.clicked.connect(self._open_profiles_file)

        profile_layout.addWidget(self.profile_combo, 0, 0, 1, 2)
        profile_layout.addWidget(self.open_profiles, 0, 2)
        profile_layout.addWidget(self.profile_details, 1, 0, 1, 3)
        profile_layout.addWidget(self.load_folder, 2, 0)
        profile_layout.addWidget(self.apply_profile, 2, 1)
        profile_layout.addWidget(self.flash_profile, 2, 2)

        layout.addWidget(self.profile_group)
        layout.addStretch(1)

        return page

    def _build_logs_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.log_group = QtWidgets.QGroupBox()
        log_layout = QtWidgets.QVBoxLayout(self.log_group)
        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(5000)
        log_layout.addWidget(self.log_view)

        action_layout = QtWidgets.QHBoxLayout()
        self.save_log = QtWidgets.QPushButton()
        self.save_log.clicked.connect(self._save_log)
        self.clear_log = QtWidgets.QPushButton()
        self.clear_log.clicked.connect(self._clear_log)
        action_layout.addWidget(self.save_log)
        action_layout.addWidget(self.clear_log)
        action_layout.addStretch(1)

        layout.addWidget(self.log_group)
        layout.addLayout(action_layout)
        layout.addStretch(1)

        return page

    def _build_settings_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.settings_group = QtWidgets.QGroupBox()
        settings_layout = QtWidgets.QVBoxLayout(self.settings_group)
        self.setting_autoscroll = QtWidgets.QCheckBox("Auto-scroll logs")
        self.setting_autoscroll.setChecked(True)
        self.setting_timestamp = QtWidgets.QCheckBox("Timestamps in logs")
        self.setting_timestamp.setChecked(True)
        settings_layout.addWidget(self.setting_autoscroll)
        settings_layout.addWidget(self.setting_timestamp)

        theme_layout = QtWidgets.QGridLayout()
        self.theme_label = QtWidgets.QLabel()
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.addItem("Odin VST", "custom")
        self.theme_combo.addItem("Qt Default", "qt")
        self.theme_combo.currentIndexChanged.connect(self._apply_theme)
        theme_layout.addWidget(self.theme_label, 0, 0)
        theme_layout.addWidget(self.theme_combo, 0, 1)

        lang_layout = QtWidgets.QGridLayout()
        self.lang_label = QtWidgets.QLabel()
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.currentIndexChanged.connect(self._apply_language)
        lang_layout.addWidget(self.lang_label, 0, 0)
        lang_layout.addWidget(self.lang_combo, 0, 1)

        settings_layout.addLayout(theme_layout)
        settings_layout.addLayout(lang_layout)

        layout.addWidget(self.settings_group)
        layout.addStretch(1)
        return page

    def _apply_settings(self) -> None:
        self.odin_path_edit.setText(self.settings.get("odin_path", _default_odin_path()))
        self.adb_path_edit.setText(self.settings.get("adb_path", _default_adb_path()))
        files = self.settings.get("files", {})
        for key, edit in self.file_edits.items():
            edit.setText(files.get(key, ""))
        flags = self.settings.get("flags", {})
        self.opt_nand_erase.setChecked(bool(flags.get("nand_erase", False)))
        self.opt_home_validate.setChecked(bool(flags.get("home_validate", False)))
        self.opt_reboot.setChecked(bool(flags.get("reboot", True)))
        self.opt_redownload.setChecked(bool(flags.get("redownload", False)))
        self.device_path_edit.setText(self.settings.get("device_path", ""))
        self.prefer_home_csc.setChecked(bool(self.settings.get("prefer_home_csc", True)))
        self.setting_autoscroll.setChecked(bool(self.settings.get("auto_scroll", True)))
        self.setting_timestamp.setChecked(bool(self.settings.get("timestamp", True)))
        theme = self.settings.get("theme", self.current_theme)
        lang = self.settings.get("language", self.current_language)
        if theme:
            for idx in range(self.theme_combo.count()):
                if self.theme_combo.itemData(idx) == theme:
                    self.theme_combo.setCurrentIndex(idx)
                    break
        if lang:
            for idx in range(self.lang_combo.count()):
                if self.lang_combo.itemData(idx) == lang:
                    self.lang_combo.setCurrentIndex(idx)
                    break
        last_profile = self.settings.get("last_profile_id", "")
        if last_profile:
            for idx in range(1, self.profile_combo.count()):
                if self.profile_combo.itemData(idx) == last_profile:
                    self.profile_combo.setCurrentIndex(idx)
                    break

    def _collect_settings(self) -> Dict:
        return {
            "odin_path": self.odin_path_edit.text().strip(),
            "adb_path": self.adb_path_edit.text().strip(),
            "files": {key: edit.text().strip() for key, edit in self.file_edits.items()},
            "flags": {
                "nand_erase": self.opt_nand_erase.isChecked(),
                "home_validate": self.opt_home_validate.isChecked(),
                "reboot": self.opt_reboot.isChecked(),
                "redownload": self.opt_redownload.isChecked(),
            },
            "device_path": self.device_path_edit.text().strip(),
            "prefer_home_csc": self.prefer_home_csc.isChecked(),
            "auto_scroll": self.setting_autoscroll.isChecked(),
            "timestamp": self.setting_timestamp.isChecked(),
            "theme": self.theme_combo.currentData(),
            "language": self.lang_combo.currentData(),
            "last_profile_id": self.profile_combo.itemData(self.profile_combo.currentIndex()) or "",
        }

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        save_settings(self._collect_settings())
        return super().closeEvent(event)

    def _log(self, message: str) -> None:
        if not message:
            return
        timestamped = message
        if self.setting_timestamp.isChecked():
            timestamp = datetime.now().strftime("%H:%M:%S")
            timestamped = f"[{timestamp}] {message}"
        self.log_lines.append(timestamped)
        if len(self.log_lines) > 5000:
            self.log_lines = self.log_lines[-5000:]
        self.log_view.appendPlainText(timestamped)
        if self.setting_autoscroll.isChecked():
            self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())

    def _clear_log(self) -> None:
        self.log_lines = []
        self.log_view.clear()

    def _save_log(self) -> None:
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, self._t("dlg_save_log"), str(APP_DIR / "odin4_gui.log")
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(self.log_lines))
            self._log(f"Log saved to {path}")
        except OSError as exc:
            self._log(f"Failed to save log: {exc}")

    def _select_odin_path(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self._t("dlg_select_odin"), str(ROOT_DIR)
        )
        if path:
            self.odin_path_edit.setText(path)
            self._refresh_command_preview()

    def _auto_detect_odin(self) -> None:
        candidate = Path(_default_odin_path())
        if candidate.exists():
            self.odin_path_edit.setText(str(candidate))
            self._log(f"Detected odin4 at {candidate}")
        else:
            self._log("odin4 not found in parent folder")
        self._refresh_command_preview()

    def _select_adb_path(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self._t("dlg_select_adb"), str(ROOT_DIR)
        )
        if path:
            self.adb_path_edit.setText(path)

    def _auto_detect_adb(self) -> None:
        adb_path = _default_adb_path()
        if adb_path:
            self.adb_path_edit.setText(adb_path)
            self._log(f"Detected adb at {adb_path}")
        else:
            self._log("adb not found in PATH")

    def _select_file(self, key: str) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self._t("dlg_select_file", key=key), str(ROOT_DIR)
        )
        if path:
            self.file_edits[key].setText(path)
            self._refresh_command_preview()

    def _clear_file(self, key: str) -> None:
        self.file_edits[key].clear()
        self._refresh_command_preview()

    def _select_firmware_folder(self) -> None:
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, self._t("dlg_select_folder"), str(ROOT_DIR)
        )
        if folder:
            self.firmware_folder_edit.setText(folder)

    def _scan_firmware_folder(self) -> None:
        folder_text = self.firmware_folder_edit.text().strip()
        if not folder_text:
            self._log("Firmware folder is empty")
            return
        folder = Path(folder_text)
        if not folder.exists():
            self._log("Firmware folder does not exist")
            return
        patterns = {
            "BL": "BL_*.tar.md5",
            "AP": "AP_*.tar.md5",
            "CP": "CP_*.tar.md5",
            "CSC": "CSC_*.tar.md5",
            "HOME_CSC": "HOME_CSC_*.tar.md5",
        }
        results = detect_firmware(folder, patterns, self.prefer_home_csc.isChecked())
        found_any = False
        for key, path in results.items():
            if path:
                self.file_edits[key].setText(str(path))
                found_any = True
        if found_any:
            self._log("Firmware auto-detect completed")
        else:
            self._log("No firmware files matched the patterns")
        self._refresh_command_preview()

    def _refresh_odin_devices(self) -> None:
        odin_path = self.odin_path_edit.text().strip()
        if not odin_path:
            self._log("Set odin4 path first")
            return
        if not Path(odin_path).exists():
            self._log("odin4 path does not exist")
            return
        self._run_process("odin4 -l", odin_path, ["-l"], self._handle_odin_devices)

    def _handle_odin_devices(self, stdout: str, stderr: str, exit_code: int) -> None:
        output = (stdout or "").strip()
        if exit_code != 0:
            self._log("odin4 -l failed")
            return
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        self.device_combo.clear()
        self.device_combo.addItem(self._t("combo_auto_device"))
        for line in lines:
            self.device_combo.addItem(line)
        self._set_device_status(len(lines))

    def _refresh_adb_devices(self) -> None:
        adb_path = self.adb_path_edit.text().strip()
        if not adb_path:
            self._log("Set adb path first")
            return
        if not Path(adb_path).exists():
            self._log("adb path does not exist")
            return
        self._run_process("adb devices", adb_path, ["devices", "-l"], self._handle_adb_devices)

    def _handle_adb_devices(self, stdout: str, stderr: str, exit_code: int) -> None:
        if exit_code != 0:
            self._log("adb devices failed")
            return
        lines = stdout.splitlines()
        devices = []
        view_lines = []
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            serial = parts[0]
            state = parts[1] if len(parts) > 1 else ""
            devices.append(serial)
            view_lines.append(line)
        self.adb_device_combo.clear()
        self.adb_device_combo.addItem(self._t("combo_all_devices"))
        for serial in devices:
            self.adb_device_combo.addItem(serial)
        self.adb_devices_view.setPlainText(
            "\n".join(view_lines) if view_lines else self._t("no_devices")
        )

    def _adb_command(self, args: List[str]) -> None:
        adb_path = self.adb_path_edit.text().strip()
        if not adb_path:
            self._log("Set adb path first")
            return
        device = self._selected_adb_device()
        full_args = []
        if device:
            full_args.extend(["-s", device])
        full_args.extend(args)
        self._run_process("adb", adb_path, full_args, None)

    def _adb_push(self) -> None:
        local_path = self.adb_push_local.text().strip()
        remote_path = self.adb_push_remote.text().strip()
        if not local_path or not remote_path:
            self._log("Push requires local and remote paths")
            return
        self._adb_command(["push", local_path, remote_path])

    def _adb_pull(self) -> None:
        remote_path = self.adb_pull_remote.text().strip()
        local_path = self.adb_pull_local.text().strip()
        if not remote_path or not local_path:
            self._log("Pull requires remote and local paths")
            return
        self._adb_command(["pull", remote_path, local_path])

    def _adb_install(self) -> None:
        apk_path = self.adb_install_apk.text().strip()
        if not apk_path:
            self._log("Select an APK file")
            return
        self._adb_command(["install", "-r", apk_path])

    def _adb_shell(self) -> None:
        cmd = self.adb_shell_cmd.text().strip()
        if not cmd:
            self._log("Enter a shell command")
            return
        self._adb_command(["shell"] + shlex.split(cmd))

    def _selected_adb_device(self) -> Optional[str]:
        index = self.adb_device_combo.currentIndex()
        if index <= 0:
            return None
        return self.adb_device_combo.currentText()

    def _select_adb_push_file(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self._t("dlg_select_push"), str(ROOT_DIR)
        )
        if path:
            self.adb_push_local.setText(path)

    def _select_adb_pull_folder(self) -> None:
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, self._t("dlg_select_pull_folder"), str(ROOT_DIR)
        )
        if folder:
            self.adb_pull_local.setText(folder)

    def _select_adb_install_apk(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self._t("dlg_select_apk"), str(ROOT_DIR), "APK (*.apk)"
        )
        if path:
            self.adb_install_apk.setText(path)

    def _profile_changed(self) -> None:
        profile = self._current_profile()
        if not profile:
            self.profile_details.setPlainText(self._t("profile_none"))
            return
        details = [
            f"{self._t('profile_name')}: {profile.name}",
            f"{self._t('profile_model')}: {profile.model}",
            f"{self._t('profile_notes')}: {profile.notes}",
            f"{self._t('profile_patterns')}:",
        ]
        for key, pattern in profile.patterns.items():
            details.append(f"  {key}: {pattern}")
        details.append(f"{self._t('profile_flags')}:")
        for key, value in profile.flags.items():
            details.append(f"  {key}: {value}")
        self.profile_details.setPlainText("\n".join(details))

    def _profile_load_folder(self) -> None:
        profile = self._current_profile()
        if not profile:
            self._log("Select a profile first")
            return
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, self._t("dlg_select_folder"), str(ROOT_DIR)
        )
        if not folder:
            return
        results = detect_firmware(Path(folder), profile.patterns, profile.default_csc_prefer_home)
        self.profile_files = {k: v for k, v in results.items() if v is not None}
        if self.profile_files:
            self._log("Profile firmware files loaded")
        else:
            self._log("No files matched profile patterns")

    def _profile_apply(self) -> bool:
        profile = self._current_profile()
        if not profile:
            self._log("Select a profile first")
            return False
        if not self.profile_files:
            self._log("Load a firmware folder first")
            return False
        for key, path in self.profile_files.items():
            if key in self.file_edits:
                self.file_edits[key].setText(str(path))
        self.opt_nand_erase.setChecked(bool(profile.flags.get("nand_erase", False)))
        self.opt_home_validate.setChecked(bool(profile.flags.get("home_validate", False)))
        self.opt_reboot.setChecked(bool(profile.flags.get("reboot", False)))
        self.opt_redownload.setChecked(bool(profile.flags.get("redownload", False)))
        self.prefer_home_csc.setChecked(bool(profile.default_csc_prefer_home))
        self._log("Profile applied to flash settings")
        return True

    def _profile_flash(self) -> None:
        if self._profile_apply():
            self._start_flash()

    def _open_profiles_file(self) -> None:
        profiles_path = _profiles_path()
        if not profiles_path.exists():
            self._log("Profiles file not found")
            return
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(profiles_path)))

    def _current_profile(self) -> Optional[Profile]:
        index = self.profile_combo.currentIndex()
        if index <= 0:
            return None
        profile_id = self.profile_combo.itemData(index)
        for profile in self.profiles:
            if profile.profile_id == profile_id:
                return profile
        return None

    def _copy_command(self) -> None:
        cmd = self.command_preview.text().strip()
        if not cmd:
            return
        QtWidgets.QApplication.clipboard().setText(cmd)
        self._log("Command copied to clipboard")

    def _build_odin_command(self) -> List[str]:
        odin_path = self.odin_path_edit.text().strip()
        if not odin_path:
            return []
        cmd = [odin_path]
        for key, flag in [("BL", "-b"), ("AP", "-a"), ("CP", "-c"), ("CSC", "-s"), ("UMS", "-u")]:
            path = self.file_edits[key].text().strip()
            if path:
                cmd.extend([flag, path])
        if self.opt_nand_erase.isChecked():
            cmd.append("-e")
        if self.opt_home_validate.isChecked():
            cmd.append("-V")
        if self.opt_reboot.isChecked():
            cmd.append("--reboot")
        if self.opt_redownload.isChecked():
            cmd.append("--redownload")

        manual_device = self.device_path_edit.text().strip()
        if manual_device:
            cmd.extend(["-d", manual_device])
        else:
            if self.device_combo.currentIndex() > 0:
                device_path = self.device_combo.currentText()
                cmd.extend(["-d", device_path])
        return cmd

    def _refresh_command_preview(self) -> None:
        cmd = self._build_odin_command()
        if not cmd:
            self.command_preview.setText("")
            return
        preview = " ".join(shlex.quote(part) for part in cmd)
        self.command_preview.setText(preview)

    def _update_flash_ready(self) -> None:
        files_set = any(edit.text().strip() for edit in self.file_edits.values())
        odin_path = self.odin_path_edit.text().strip()
        odin_ok = bool(odin_path) and Path(odin_path).exists()
        ready = files_set and self.confirm_risk.isChecked() and self.confirm_download.isChecked() and odin_ok
        self.flash_button.setEnabled(ready and self.flash_process is None)

    def _start_flash(self) -> None:
        if self.flash_process is not None:
            self._log("Flash already in progress")
            return
        cmd = self._build_odin_command()
        if not cmd:
            self._log("Build a command first")
            return
        odin_path = cmd[0]
        if not Path(odin_path).exists():
            self._log("odin4 path does not exist")
            return
        if not any(edit.text().strip() for edit in self.file_edits.values()):
            self._log("Select at least one firmware file")
            return
        confirm = QtWidgets.QMessageBox.warning(
            self,
            self._t("dlg_confirm_title"),
            self._t("dlg_confirm_text"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return
        self._log(f"Starting flash: {' '.join(cmd)}")
        self._set_status("flashing")
        self.flash_progress.setRange(0, 0)
        self.flash_process = self._run_process("odin4", cmd[0], cmd[1:], self._flash_finished, is_flash=True)
        self.flash_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def _flash_finished(self, stdout: str, stderr: str, exit_code: int) -> None:
        self._log(f"Flash finished with code {exit_code}")
        self._set_status("idle")
        self.flash_progress.setRange(0, 1)
        self.flash_progress.setValue(0)
        self.flash_process = None
        self.stop_button.setEnabled(False)
        self._update_flash_ready()

    def _stop_flash(self) -> None:
        if self.flash_process is None:
            return
        self._log("Stopping flash process")
        self.flash_process.kill()
        self.flash_process = None
        self._set_status("idle")
        self.flash_progress.setRange(0, 1)
        self.flash_progress.setValue(0)
        self.stop_button.setEnabled(False)
        self._update_flash_ready()

    def _run_process(
        self,
        name: str,
        program: str,
        args: List[str],
        on_finish,
        is_flash: bool = False,
    ) -> QtCore.QProcess:
        process = QtCore.QProcess(self)
        process.setProgram(program)
        process.setArguments(args)
        process.setWorkingDirectory(str(ROOT_DIR))
        process.setProcessChannelMode(QtCore.QProcess.SeparateChannels)
        process._stdout = ""
        process._stderr = ""

        def handle_output(is_error: bool) -> None:
            if is_error:
                data = process.readAllStandardError()
            else:
                data = process.readAllStandardOutput()
            text = bytes(data).decode("utf-8", errors="replace")
            if not text:
                return
            for line in text.splitlines():
                if line.strip():
                    self._log(line.strip())
            if is_error:
                process._stderr += text
            else:
                process._stdout += text

        process.readyReadStandardOutput.connect(lambda: handle_output(False))
        process.readyReadStandardError.connect(lambda: handle_output(True))

        def finished(exit_code: int, _status: QtCore.QProcess.ExitStatus) -> None:
            if on_finish:
                on_finish(process._stdout, process._stderr, exit_code)
            if process in self.other_processes:
                self.other_processes.remove(process)
            process.deleteLater()

        process.finished.connect(finished)
        process.errorOccurred.connect(lambda err: self._log(f"Process error: {err}"))

        process.start()
        if not is_flash:
            self.other_processes.append(process)
        return process


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("odin")
    signal.signal(signal.SIGINT, lambda *_args: app.quit())
    sig_timer = QtCore.QTimer()
    sig_timer.start(200)
    sig_timer.timeout.connect(lambda: None)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
