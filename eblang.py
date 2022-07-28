import os, sys


# Память в режиме интерпритации - словарь из переменных
memory = {
    '__name__': {
        'type': 'const_str',
        'data': str(__name__)
    }
}

line_ptr = 0


# В случае ошибки - аварийный дамп память 
def err(message):
    print(f"ERROR:{message}")
    print(f"Memory:{memory}")
    print(f"Line:{line_ptr}")
    exit(-1)


# Выполнение команд с аргументами
def execute(command, param1 = None, param2 = None, param3 = None):
    if command == 1:    # echo
        if param1 in memory.keys():
            print(
                memory.get(param1)['data']
                )
    elif command == 2:  # string
        if param1 in memory.keys():
            if memory.get(param1)['type'] == "str":
                print(
                    param1,     # Имя переменной
                    param2      # Данные переменной
                    )
                memory.get(param1)['data'] = param2
            else:
                err(f"Типы данных не соответствуют: {param2}[{type(param2)}] и string")
        else:
            memory.update(
                dict.fromkeys([param1],
                {
                    'type': "str", 
                    'data': param2
                }
                    ))
    elif command == 3:  # int
        if param1 in memory.keys():
            if memory.get(param1)['type'] == "int":
                print(
                    param1,     # Имя переменной
                    param2      # Данные переменной
                    )
                memory.get(param1)['data'] = param2
            else:
                err(f"Типы данных не соответствуют: {param2}[{type(param2)}] и int")
        else:
            memory.update(
                dict.fromkeys([param1],
                {
                    'type': "int", 
                    'data': param2
                }
                    ))
    elif command == 4:  # sum
        if param1 in memory.keys() and param2 in memory.keys() and param3 in memory.keys():
            if memory.get(param1)['type'] == "int" and memory.get(param2)['type'] == "int" and memory.get(param3)['type'] == "int":
                print(
                    param1,     # Имя переменной
                    param2      # Данные переменной
                    )
                memory.get(param1)['data'] = param2
            else:
                err(f"Типы данных не соответствуют: {memory.get(param1)['type']} и {memory.get(param2)['type']}")
        else:
            err(f"Переменные не найдены: {param1} и {param2}")


# Парсинг
def parse(file):
    f = open(file, 'r')
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
        if(line.strip()[0] != '#'):
            programm_raw.append(line.strip().split(':'))
    
    return programm_raw


# Анализ команд
def analyze(data):
    for i in data:
        command = -1

        if i[0] == 'echo':
            execute(1, i[1])
        elif i[0] == 'string':
            execute(2, i[1].split(',')[0], i[1].split(',')[1])
        elif i[0] == 'int':
            execute(3, i[1].split(',')[0], i[1].split(',')[1])
        elif i[0] == 'sum':
            execute(4, i[1].split(',')[0], i[1].split(',')[1], i[1].split(',')[0])
        elif i[0] == 'meminfo':
            print(memory)
        else:
            err(f"Инструкция: {i[0]}, не распознанна")


# Обработка аргументов
if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            analyze(parse(sys.argv[i]))