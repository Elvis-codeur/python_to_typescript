set CURRENT_DIR=%cd%
echo %CURRENT_DIR%
call "D:\projet_github\FOR GOD\Transcribe project\python virtualenv\virtualenv\Scripts\activate"
py --version 
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
