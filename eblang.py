# -*- coding: utf-8 -*-
import os
import sys
from enum import Enum, auto


class OpCode(Enum):
    ECHO_VAR = auto()  # Вывести переменную из памяти.
    STORE_STRING = auto()  # Сохранить строку в память.
    STORE_INTEGER = auto()  # Положить число в память.
    MATH_SUM_VARS = auto()  # Сложить три числовых переменных.
    MATH_SUB_VARS = auto()  # Вычесть три числовых переменных.
    H9QP = auto()  # ...


# Память в режиме интерпретации - словарь из переменных
memory = {"__name__": {"type": "const_str", "data": str(__name__)}}

line_ptr = 0
file_ptr = ""


def bottle_or_bottles(num_bottles):
    if num_bottles != 1:
        return "bottles"
    return "bottle"


def song1(num_bottles=99):
    verse1 = "{0} {1} of beer on the wall, {0} {1} of beer."
    verse2 = "Take one down and pass it around, {} {} of beer on the wall"

    for i in range(num_bottles, 0, -1):
        # Первая часть
        print(verse1.format(i, bottle_or_bottles(i)))
        # Вторая часть
        num_bottles_next = i - 1
        if num_bottles_next == 0:
            num_bottles_next = "no more"
        print(verse2.format(num_bottles_next, bottle_or_bottles(num_bottles_next)))

    print(
        "No more bottles of beer on the wall, no more bottles of beer.\n"
        "Go to the store and buy some more, {} bottles of beer on "
        "the wall".format(num_bottles)
    )


def _99bottles():
    song1()


# Выключение устройства
def suicide():
    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        print("sudo Shutdown PC, please")
        os.system("shutdown now -h")
        os.system("systemctl poweroff")
    elif sys.platform == "darwin":
        # OS X
        print(":/ shutdown your computer manualy, rich bitch!")
    elif sys.platform == "win32" or sys.platform == "win64":
        # windows
        print("Shutdown PC, please")
        os.system("shutdown /s /t 1")
    else:
        err(f"Платформа {sys.platform} не поддерживается")


# В случае ошибки - аварийный дамп память
def err(message):
    print(f"ERROR:{message}")
    print(f"Memory:{memory}")
    print(f"Line:{line_ptr}")
    exit(-1)


# Выполнение команд с аргументами
def execute(command, param1=None, param2=None, param3=None):
    if command == OpCode.ECHO_VAR:
        if param1 in memory.keys():
            print(memory.get(param1)["data"])
    elif command == OpCode.STORE_STRING:
        if param1 in memory.keys():
            if memory.get(param1)["type"] == "str":
                print(param1, param2)  # Имя переменной  # Данные переменной
                memory.get(param1)["data"] = param2
            else:
                err(f"Типы данных не соответствуют: {param2}[{type(param2)}] и string")
        else:
            memory.update(dict.fromkeys([param1], {"type": "str", "data": param2}))
    elif command == OpCode.STORE_INTEGER:
        if param1 in memory.keys():
            if memory.get(param1)["type"] == "int":
                print(param1, param2)  # Имя переменной  # Данные переменной
                memory.get(param1)["data"] = param2
            else:
                err(f"Типы данных не соответствуют: {param2}[{type(param2)}] и int")
        else:
            memory.update(dict.fromkeys([param1], {"type": "int", "data": param2}))
    elif command == OpCode.MATH_SUM_VARS:
        if (
            param1 in memory.keys()
            and param2 in memory.keys()
            and param3 in memory.keys()
        ):
            if (
                memory.get(param1)["type"] == "int"
                and memory.get(param2)["type"] == "int"
                and memory.get(param3)["type"] == "int"
            ):
                # param1 = param2 +  param3
                memory.get(param1)["data"] = int(memory.get(param2)["data"]) + int(
                    memory.get(param3)["data"]
                )
            else:
                err(
                    f"Типы данных не соответствуют: {memory.get(param1)['type']}, {memory.get(param2)['type']}, {memory.get(param3)['type']}"
                )
        else:
            err(f"Переменные не найдены: {param1}, {param2}, {param3}")
    elif command == OpCode.MATH_SUB_VARS:
        if (
            param1 in memory.keys()
            and param2 in memory.keys()
            and param3 in memory.keys()
        ):
            if (
                memory.get(param1)["type"] == "int"
                and memory.get(param2)["type"] == "int"
                and memory.get(param3)["type"] == "int"
            ):
                # param1 = param2 - param3
                memory.get(param1)["data"] = int(memory.get(param2)["data"]) - int(
                    memory.get(param3)["data"]
                )
            else:
                err(
                    f"Типы данных не соответствуют: {memory.get(param1)['type']}, {memory.get(param2)['type']}, {memory.get(param3)['type']}"
                )
        else:
            err(f"Переменные не найдены: {param1}, {param2}, {param3}")
    elif command == OpCode.H9QP:
        for i in param1:
            if i == "H":
                print("Hello World!")
            elif i == "Q":
                print(param1)
            elif i == "9":
                print(_99bottles())


# Парсинг
def parse(file):
    f = open(file, "r", encoding="utf-8")
    programm_raw = []

    while True:
        # считываем строку
        line = f.readline()

        # Прерываем цикл, если читать нечего
        if not line:
            f.close
            break

        # Если строка не содержит ничего - пропускаем
        if len(line.strip()) < 1:
            continue

        # Если строка не содержит комментарий - добавляем её в список
        if line.strip()[0] != "#":
            programm_raw.append(line.strip().split(":"))

    return programm_raw


# Анализ команд
def analyze(data):
    for i in data:
        operation = i[0]
        if operation == "echo":
            execute(OpCode.ECHO_VAR, i[1])
        elif operation == "string":
            execute(OpCode.STORE_STRING, i[1].split(",")[0], i[1].split(",")[1])
        elif operation == "int":
            execute(OpCode.STORE_INTEGER, i[1].split(",")[0], i[1].split(",")[1])
        elif operation == "sum":
            execute(
                OpCode.MATH_SUM_VARS,
                i[1].split(",")[0],
                i[1].split(",")[1],
                i[1].split(",")[2],
            )
        elif operation == "sub":
            execute(
                OpCode.MATH_SUB_VARS,
                i[1].split(",")[0],
                i[1].split(",")[1],
                i[1].split(",")[2],
            )
        elif operation == "HQ9":
            execute(OpCode.H9QP, i[1])
        elif operation == "meminfo":
            print(memory)
        elif operation == "quine":
            f = open(file_ptr, "r", encoding="utf-8")
            print(f.read())
            f.close
        elif operation == "suicide":
            suicide()
        else:
            err(f"Инструкция: {operation}, не распознанна")


# Обработка аргументов
if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            file_ptr = sys.argv[i]
            analyze(parse(file_ptr))
