# Практична робота № 5

Навчальні вебпроєкти на Django та Flask. Для запуску потрібен Python 3.10 або новіший. Команди виконуйте з каталогу PR05 після розпакування архіву.

## Підготовка у Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
where.exe python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python practical_05_task_1_1.py
python practical_05_task_1_2.py --check
```

На Linux або macOS для створення й активації використайте `python3 -m venv venv` і `source venv/bin/activate`. Шлях до інтерпретатора покаже `which python`.

Якщо PowerShell блокує скрипт активації, відкрийте CMD і виконайте `venv\Scripts\activate.bat` або запускайте команди через `.\venv\Scripts\python.exe`.

## Відтворення середовища

Після `deactivate` створіть середовище `venv2`, активуйте його так само та виконайте:

```text
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python practical_05_task_1_2.py --check
```

Щоб згенерувати список окремим файлом, виконайте `python practical_05_task_1_2.py --file requirements_generated.txt`.

## Запуск Django

```text
python mysite/manage.py migrate
python mysite/manage.py runserver
```

- Головна — http://127.0.0.1:8000/
- Про проєкт — http://127.0.0.1:8000/about/
- Контакт — http://127.0.0.1:8000/contact/
- Персональне привітання — http://127.0.0.1:8000/contact/?name=Ілля

## Запуск Flask

В окремому терміналі активуйте середовище і виконайте `python myflaskapp/app.py`. Також працює команда `python -m flask --app "myflaskapp.app:create_app('development')" --debug run --port 5000`.

- Головна — http://127.0.0.1:5000/
- Про додаток — http://127.0.0.1:5000/about
- JSON API — http://127.0.0.1:5000/api/info
- Привітання — http://127.0.0.1:5000/greet/Ілля або http://127.0.0.1:5000/greet?name=Ілля

## Аналіз конфігурації та структури

```text
python practical_05_task_2_2.py
python practical_05_task_3_2.py
```

Для налаштування Django через середовище доступні `DJANGO_DEBUG`, `DJANGO_SECRET_KEY` і `DJANGO_ALLOWED_HOSTS`. Конфігурація Flask `production` читає `FLASK_SECRET_KEY`.
