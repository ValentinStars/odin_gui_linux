# odin

PySide6 GUI‑оболочка для `odin4` с ADB‑инструментами, профилями и логами.

## Возможности
- Полный набор флагов `odin4`.
- Автопоиск файлов прошивки по папке.
- Профили устройств и «Flash Stock».
- ADB: список устройств, reboot, push/pull, install APK, shell‑команды.
- Логи в реальном времени и экспорт.
- Тема (Qt Default / Odin VST) и язык (RU / EN).

## Запуск
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## One‑file сборка
```bash
pyinstaller --noconfirm --onefile --windowed \
  --name "odin" \
  --add-data "theme.qss:." \
  --add-data "profiles/devices.json:profiles" \
  --add-binary "../odin4:." \
  --add-binary "../adb:." \
  main.py
```

## Безопасность
Прошивка может повредить устройство. Используйте на свой риск.

## Конфигурация
Настройки и профили сохраняются в `~/.config/odin/`.
