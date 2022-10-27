# Домашнее задание к лекции «Aiohttp»

Инструкцию по сдаче домашнего задания вы найдете на главной странице репозитория. 

## Задание 1

Вам нужно написать REST API (backend) для сайта объявлений.

Должны быть реализованы методы создания/удаления/редактирования объявления.    

У объявления должны быть следующие поля: 
- заголовок
- описание
- дата создания
- владелец

Результатом работы является API, написанное на aiohttp.

Этапы выполнения задания:

1. Сделайте роут на aiohttp.
2. POST метод должен создавать объявление, GET - получать объявление, DELETE - удалять объявление.

## Задание 2 *(не обязательное)

Докеризировать API, написанный в задании 1.
Чтобы проверить корректность работы сервиса, нужно:

1. Запустить контейнер
2. Проверить работу роута