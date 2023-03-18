#!/bin/bash

# Проверяем существование файла config.py
if [ -f configs_/config.py ]; then
  echo "Файл существует. Нажмите enter..."; read a;
else
  # Создаём папку configs_
  mkdir configs_
  # Переходим в неё
  cd configs_
  echo "Введите TELEGRAM_TOKEN:"
  read a
  echo "Введите TELEGRAPH_TOKEN:"
  read b
  echo "Введите TELEGRAM_AUTHOR:"
  read c
  # Создаём файл config.py и записываем функции
  echo "def TELEGRAM_TOKEN():
    return '"$a"'

def TELEGRAPH_TOKEN():
    return '"$b"'

def TELEGRAPH_AUTHOR():
    return '"$c"'" > config.py

  # Сообщаем пользователю, что файл создан
  echo "Файл configs_/config.py создан. Нажмите enter..."; read a;
fi
