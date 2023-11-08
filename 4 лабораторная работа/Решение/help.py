import json
def AddDatePrint(s="Неверный формат. Введите дату в формате дд.мм.гггг: ", end=""):
    print(s)
    date = input()
    dateMas = date.split(".")
    return date, dateMas


def AddDateFirstCheck(date, dateMas):
    while len(dateMas) != 3:
        date, dateMas = AddDatePrint()
    return date, dateMas


def AddDateSecondCheck(date, dateMas):
    while len(dateMas[0]) != 2 or len(dateMas[1]) != 2 or len(dateMas[2]) != 4:
        date, dateMas = AddDatePrint()
        date, dateMas = AddDateFirstCheck(date, dateMas)
    return date, dateMas


def AddDateThirdChekc(date, dateMas):
    while not dateMas[0].isdigit() or not dateMas[1].isdigit() or not dateMas[2].isdigit():
        date, dateMas = AddDatePrint()
        date, dateMas = AddDateFirstCheck(date, dateMas)
        date, dateMas = AddDateSecondCheck(date, dateMas)
    return date, dateMas


def AddDate(s="Введите дату в формате дд.мм.гггг"):
    date, dateMas = AddDatePrint(s)
    date, dateMas = AddDateFirstCheck(date, dateMas)
    date, dateMas = AddDateSecondCheck(date, dateMas)
    date, dateMas = AddDateThirdChekc(date, dateMas)
    while 0 >= int(dateMas[0]) or int(dateMas[0]) > 31 or int(dateMas[1]) > 12 or int(dateMas[1]) < 1 or \
            int(dateMas[0]) > 29 and int(dateMas[1]) == 2:
        if int(dateMas[0]) > 29 and int(dateMas[1]) == 2:
            date, dateMas = AddDatePrint("В феврале не может быть больше 29 дней! Введите дату заново: ", end="")
        elif int(dateMas[0]) <= 0:
            date, dateMas = AddDatePrint("Количество дней должно быть больше 0! Введите дату заново: ", end="")
        elif int(dateMas[0]) > 31:
            date, dateMas = AddDatePrint("Количество дней не может быть больше 31! Введите дату заново: ", end="")
        elif int(dateMas[1]) > 12:
            date, dateMas = AddDatePrint("Количество месяцов не может быть больше 12! Введите дату заново: ", end="")
        elif int(dateMas[1] < 1):
            date, dateMas = AddDatePrint("Количество месяцов не может быть меньше 1! Введите дату заново: ", end="")
        date, dateMas = AddDateFirstCheck(date, dateMas)
        date, dateMas = AddDateSecondCheck(date, dateMas)
        date, dateMas = AddDateThirdChekc(date, dateMas)
    return date

busList = list()
busDict = dict()
busDownDict = dict()

driversDict = dict()
driversList = list()
driversDownDict = dict()
driversDownDownDict = dict()
driversDownList = list()

def AddBuses():
    busDownDict = dict()
    print("Введите id: ", end="")
    id = input()
    for i in range(len(busList)):
        while (busList[i]["id"] == id):
            print("Такой id автобуса уже существует, введите другой id: ", end="")
            id = input()
    print("Введите Гос.номер: ", end="")
    number = input()
    print("Введите маршрут: ", end="")
    route = input()
    todate = AddDate()
    busDownDict["id"] = id
    busDownDict["Гос. номер"] = number
    busDownDict["Маршрут"] = route
    busDownDict["Дата ТО"] = todate
    busList.append(busDownDict)
    busDict["Автобусы"] = busList
def AddDrivers():
    driversDownList = list()
    print("Введите ФИО водителя, которого хотите добавить: ", end="")
    fio = input()
    for i in range(len(driversList)):
        while driversList[i]["ФИО"] == fio:
            print("Водитель с таким же ФИО уже есть в списке, введите ФИО заново")
            fio = input()
    print("Введите id автобуса: ", end="")
    id = input()
    tempListId = list()
    for i in range(len(busList)):
        tempListId.append(busList[i]["id"])
    while id not in tempListId:
        print(f"id автобуса {id} не найден. Введите id автобуса заново: ", end="")
        id = input()
    dateDep = AddDate("Введите дату выезда в формате дд.мм.гггг: ")
    datePas = AddDate("Введите дату сдачи смены в формате дд.мм.гггг: ")
    driversDownDict["ФИО"] = fio
    driversDownDownDict["Дата выезда"] = dateDep
    driversDownDownDict["Дата сдачи смены"] = datePas
    idn = tempListId.index(id)
    tempDict = dict()
    tempDict = driversDownDownDict
    tempDict.update(busList[idn])
    driversDownList.append(tempDict)
    driversDownDict["История"] = driversDownList
    driversList.append(driversDownDict)
    driversDict["Водители"] = driversList
def ChangeBuses():
    print("Введите id автобуса, данные которого вы хотите изменить: ", end="")
    id = input()
    isFind = False
    for i in range(len(busList)):
        if busList[i]["id"] == id:
            isFind = True
            index = i
            break
    if not isFind:
        print("Автобус с таким id не найден")
    else:
        print("Введите, что вы хотите изменить\n"
              "1. id\n"
              "2. Гос. номер\n"
              "3. Маршрут\n"
              "4. Дату ТО")
        answer = input()
        while answer != "1" and answer != "2" and answer != "3" and answer != "4":
            print("Введите число от 1 до 4")
            answer = input()
        if answer == "1":
            print("Введите новое id: ", end="")
            id = input()
            for i in range(len(busList)):
                while busList[i]["id"] == id:
                    print("Такое id уже существует, введите другое id: ", end="")
                    id = input()
            busList[index]["id"] = id
            print("id изменено")
        if answer == "2":
            print("Введите новый гос. номер: ", end="")
            number = input()
            busList[index]["Гос. номер"] = number
            print("Гос. номер изменён")
        if answer == "3":
            print("Введите новый маршрут: ", end="")
            route = input()
            busList[index]["Маршрут"] = route
            print("Маршрут изменён")
        if answer == "4":
            date = AddDate("Введите новую дату ТО в формате дд.мм.гггг")
            busList[index]["Дата ТО"] = date
            print("Дата ТО изменена")

AddBuses()
AddDrivers()
AddDrivers()
print(busDict)
print(busList)