# odin

Графический интерфейс для `odin4` на PySide6 с дополнительными ADB‑инструментами.

## Возможности
- Полный набор флагов `odin4`: `-b/-a/-c/-s/-u`, `-e`, `-V`, `--reboot`, `--redownload`, выбор устройства `-d`.
- Автопоиск файлов прошивки по папке (BL/AP/CP/CSC/HOME_CSC).
- Профили устройств и кнопка «Flash Stock».
- ADB‑инструменты: список устройств, reboot, push/pull, install APK, shell‑команды.
- Логи в реальном времени, экспорт логов.
- Переключение темы (Qt Default / Odin VST) и языка (RU / EN).

## Требования
- Linux.
- `odin4` рядом с проектом или в одном бинарнике.
- `adb` в PATH или рядом с проектом / внутри одного бинарника.

## Запуск (из исходников)
```bash
cd odin4_gui
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## One‑file сборка (PyInstaller)
```bash
cd odin4_gui
. .venv/bin/activate
pyinstaller --noconfirm --onefile --windowed \
  --name "odin" \
  --add-data "theme.qss:." \
  --add-data "profiles/devices.json:profiles" \
  --add-binary "../odin4:." \
  --add-binary "../adb:." \
  main.py
```

Результат: `odin4_gui/dist/odin`

## Структура
- `odin4_gui/main.py` — основной GUI
- `odin4_gui/theme.qss` — тема Odin VST
- `odin4_gui/profiles/devices.json` — профили устройств

## Конфигурация
Пользовательские настройки и профили копируются в каталог конфигурации Qt.

- Linux: `~/.config/odin/`

## Примечания
Файлы прошивок и бинарники `odin4`/`adb` в репозиторий не включаются.

## Автор
Valentin Stars

## Лицензия
MIT (см. `LICENSE`).
