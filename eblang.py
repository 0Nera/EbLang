# -*- coding: utf-8 -*-
import os
import sys
import typing
from enum import Enum, auto


class OpCode(Enum):
    """
    Тип инструкции (operation code) для интерпретатора.
    """

    ECHO_VAR = auto()  # Вывести переменную из памяти.
    STORE_STRING = auto()  # Сохранить строку в память.
    STORE_INTEGER = auto()  # Положить число в память.
    MATH_SUM_VARS = auto()  # Сложить три числовых переменных.
    MATH_SUB_VARS = auto()  # Вычесть три числовых переменных.
    H9QP = auto()  # ...
    MEMORY_INFO = auto()  # ...
    QUINE = auto()  # ...


class Operation:
    """
    Инструкция (операция).
    """

    # Код операции.
    opcode: OpCode

    # Операнды.
    operands: list

    def __init__(self, opcode: OpCode, operands: typing.Optional[typing.List] = None):
        self.opcode = opcode
        self.operands = operands if operands is not None else []


def lexer_tokenize(filepath: str):
    """
    Токенизация, разделение на токены языка.
    """

    # TODO: Переработка лексера, в частности процесса токенизации, работает плохо.
    with open(filepath, "r", encoding="utf-8") as f:
        while True:
            # Строка из файла
            line = f.readline()

            # Больше нет строк.
            if not line:
                break

            # Пустая строка
            line = line.strip()
            if len(line) < 1:
                continue

            # Комментарий.
            if line.startswith("#"):
                continue

            yield line.split(":")


def parser_parse(optokens: typing.List[str]):
    """
    Парсинг, приведение *токенов* языка после токенизации к операции с явно указанными операндами.
    """
    for optoken in optokens:
        # optoken -> кортеж операции после токенизации.

        # Сама операция (строка пользователя).
        operation = optoken[0]
        if len(optoken) < 2:
            err("Недостаточно операндов! (Вы забыли `:`?)")
        raw_operand_str = optoken[1]
        operands = raw_operand_str.split(",")

        if operation == "echo":
            yield Operation(OpCode.ECHO_VAR, [raw_operand_str])
        elif operation == "string":
            yield Operation(OpCode.STORE_STRING, [operands[0], operands[1]])
        elif operation == "int":
            yield Operation(OpCode.STORE_INTEGER, [operands[0], operands[1]])
        elif operation == "sum":
            yield Operation(
                OpCode.MATH_SUM_VARS, [operands[0], operands[1], operands[2]]
            )
        elif operation == "sub":
            yield Operation(
                OpCode.MATH_SUB_VARS, [operands[0], operands[1], operands[2]]
            )
        elif operation == "HQ9":
            yield Operation(OpCode.H9QP, [raw_operand_str])
        elif operation == "meminfo":
            yield Operation(OpCode.MEMORY_INFO)
        elif operation == "quine":
            yield Operation(OpCode.QUINE)
        elif operation == "suicide":
            yield Operation(OpCode.SUICIDE)
        else:
            err(f"Не удалось распознать инструкцию: `{operation}`!")


def run_operations_interpreter(operations: typing.List[Operation]):
    for operation in operations:
        execute_operation(operation)


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
def execute_operation(operation: Operation):
    opcode = operation.opcode
    if opcode == OpCode.ECHO_VAR:
        if len(operation.operands) < 1:
            err("Недостаточно аргументов для ECHO_VAR!")
        operand_a = operation.operands[0]
        if operand_a in memory.keys():
            print(memory.get(operand_a)["data"])
    elif opcode == OpCode.STORE_STRING:
        if len(operation.operands) < 2:
            err("Недостаточно аргументов для STORE_STRING!")
        operand_a = operation.operands[0]
        operand_b = operation.operands[1]
        if operand_a in memory.keys():
            if memory.get(operand_a)["type"] == "str":
                print(operand_a, operand_b)  # Имя переменной  # Данные переменной
                memory.get(operand_a)["data"] = operand_b
            else:
                err(
                    f"Типы данных не соответствуют: {operand_b}[{type(operand_b)}] и string"
                )
        else:
            memory.update(
                dict.fromkeys([operand_a], {"type": "str", "data": operand_b})
            )
    elif opcode == OpCode.STORE_INTEGER:
        if len(operation.operands) < 2:
            err("Недостаточно аргументов для STORE_INTEGER!")
        operand_a = operation.operands[0]
        operand_b = operation.operands[1]
        if operand_a in memory.keys():
            if memory.get(operand_a)["type"] == "int":
                print(operand_a, operand_b)  # Имя переменной  # Данные переменной
                memory.get(operand_a)["data"] = operand_b
            else:
                err(
                    f"Типы данных не соответствуют: {operand_b}[{type(operand_b)}] и int"
                )
        else:
            memory.update(
                dict.fromkeys([operand_a], {"type": "int", "data": operand_b})
            )
    elif opcode == OpCode.MATH_SUM_VARS:
        if len(operation.operands) < 3:
            err("Недостаточно аргументов для MATH_SUM_VARS!")
        operand_a = operation.operands[0]
        operand_b = operation.operands[1]
        operand_c = operation.operands[2]
        if (
            operand_a in memory.keys()
            and operand_b in memory.keys()
            and operand_c in memory.keys()
        ):
            if (
                memory.get(operand_a)["type"] == "int"
                and memory.get(operand_b)["type"] == "int"
                and memory.get(operand_c)["type"] == "int"
            ):
                # operand_a = operand_b +  operand_c
                memory.get(operand_a)["data"] = int(
                    memory.get(operand_b)["data"]
                ) + int(memory.get(operand_c)["data"])
            else:
                err(
                    f"Типы данных не соответствуют: {memory.get(operand_a)['type']}, {memory.get(operand_b)['type']}, {memory.get(operand_c)['type']}"
                )
        else:
            err(f"Переменные не найдены: {operand_a}, {operand_b}, {operand_c}")
    elif opcode == OpCode.MATH_SUB_VARS:
        if len(operation.operands) < 3:
            err("Недостаточно аргументов для MATH_SUB_VARS!")
        operand_a = operation.operands[0]
        operand_b = operation.operands[1]
        operand_c = operation.operands[2]
        if (
            operand_a in memory.keys()
            and operand_b in memory.keys()
            and operand_c in memory.keys()
        ):
            if (
                memory.get(operand_a)["type"] == "int"
                and memory.get(operand_b)["type"] == "int"
                and memory.get(operand_c)["type"] == "int"
            ):
                # operand_a = operand_b - operand_c
                memory.get(operand_a)["data"] = int(
                    memory.get(operand_b)["data"]
                ) - int(memory.get(operand_c)["data"])
            else:
                err(
                    f"Типы данных не соответствуют: {memory.get(operand_a)['type']}, {memory.get(operand_b)['type']}, {memory.get(operand_c)['type']}"
                )
        else:
            err(f"Переменные не найдены: {operand_a}, {operand_b}, {operand_c}")
    elif opcode == OpCode.H9QP:
        if len(operation.operands) < 1:
            err("Недостаточно аргументов для H9QP!")
        operand_a = operation.operands[0]
        for i in operand_a:
            if i == "H":
                print("Hello World!")
            elif i == "Q":
                print(operand_a)
            elif i == "9":
                print(_99bottles())
    elif opcode == OpCode.MEMORY_INFO:
        print(memory)
    elif opcode == OpCode.QUINE:
        with open(file_ptr, "r", encoding="utf-8") as f:
            print(f.read())
    elif opcode == OpCode.SUICIDE:
        suicide()
    else:
        err(f"Ошибка на стороне парсера! Получен неизвестный opcode `{opcode}`!")


# Обработка аргументов
if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            file_ptr = sys.argv[i]

            print(f"Токенизирую файл `{file_ptr}` !")
            tokens = lexer_tokenize(file_ptr)
            print(f"Парсинга файла...")
            operations = parser_parse(tokens)
            print(f"Начинаю исполнять операции...")
            print(f"Вывод: \n")
            run_operations_interpreter(operations)
