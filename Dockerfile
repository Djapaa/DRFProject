FROM python:3.10-alpine3.19
LABEL authors="esteb"





#src будет являться рабочей директорией,
#рабочая директория нужна для того,
#чтобы команды которые мы пошлем в докер запускались из этой директории(чтобы не писать полный пусть до manage.py)
WORKDIR /src

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Пробрасываем порт
EXPOSE 8000

#Пакеты которые необходимо установить в линуксе чтобы подключиться к postgres
RUN apk add postgresql-client build-base postgresql-dev


#Создаем пользователя в ОС без пароля с именем service-user
RUN adduser --disabled-password service-user


#запуск команд будет под созданным пользователем
USER service-user


#Копируем зависимости
COPY requirements.txt /temp/requirements.txt

#Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt


#Копируем папку проекта, в этой папке будет лежать проект Django
COPY src /src