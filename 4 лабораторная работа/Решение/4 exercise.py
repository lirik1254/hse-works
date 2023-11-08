import json
from datetime import datetime


def CheckDate():
    print("Введите день: ", end="")
    day = input()
    while not day.isdigit() or day[0] == "0" or int(day) < 1 or int(day) > 31:
        if not day.isdigit():
            print("Введите целое число больше 0 и меньше 32! ", end="")
            day = input()
        elif day[0] == "0":
            print(f"Недопустимое значение {day} для кол-ва дней, введите кол-во дней заново: ", end="")
            day = input()
        else:
            print("Кол-во дней должно быть в диапазоне от 1 до 31! Введите кол-во дней заново: ", end="")
            day = input()
    print("Введите месяц (целое число от 1 до 12): ", end="")
    month = input()
    while not month.isdigit() or month[0] == "0" or int(month) < 1 or int(month) > 12:
        if not month.isdigit():
            print("Введите целое, положительное число меньше 13! ", end="")
            month = input()
        else:
            print(f"Недопустимое значение '{month}' для месяца. Введите заново: ", end="")
            month = input()
    print("Введите год: ", end = "")
    year = input()
    while not year.isdigit() or year[0] == "0" or int(year) > 9999:
        if not year.isdigit() or int(year) > 9999:
            print("Введите целое неотрицательное число меньше 10000: ", end = "")
            year = input()
        else:
            print("Год не может начинаться с 0, введите год заново: ", end = "")
            year = input()
    while True:
        try:
            date = datetime(int(year), int(month), int(day))
            return date
        except BaseException:
            print(f"В {month} месяце {year} года не может быть {day} дней. Введите значение заново: ", end = "")
            day = input()


def StrCheckDate():
    date = CheckDate()
    if date.day < 10 and date.month < 10:
        date = "0" + str(date.day) + "." + "0" + str(date.month) + "." + str(date.year)
    elif date.day < 10:
        date = "0" + str(date.day) + "." + str(date.month) + "." + str(date.year)
    elif date.month < 10:
        date = str(date.day) + "." + "0" + str(date.month) + "." + str(date.year)
    else:
        date = str(date.day) + "." + str(date.month) + "." + str(date.year)
    return date


busDict = dict()
busList = list()
busDownDict = dict()

driversDict = dict()
driversList = list()
driversDownDict = dict()
driversDownList = list()
driversDownDownDict = dict()

date = ""
dateMas = list()
driversDictFirst = dict()
driversListFirst = list()

busListCopy = list()
driversListCopy = list()


def RewriteCopy():
    global busListCopy
    global driversListCopy
    busListCopy = busList.copy()
    driversListCopy = driversList.copy()
    for i in range(len(busList)):
        busListCopy[i] = busList[i].copy()
    for i in range(len(driversList)):
        driversListCopy[i] = driversList[i].copy()
        driversListCopy[i]["История"] = driversList[i]["История"].copy()
        for g in range(len(driversList[i]["История"])):
            driversListCopy[i]["История"][g] = driversList[i]["История"][g].copy()


def RewriteMain():
    global busList
    global driversList
    busList = busListCopy.copy()
    driversList = driversListCopy.copy()
    for i in range(len(busListCopy)):
        busList[i] = busListCopy[i].copy()
    for i in range(len(driversListCopy)):
        driversList[i] = driversListCopy[i].copy()
        driversList[i]["История"] = driversListCopy[i]["История"].copy()
        for g in range(len(driversListCopy[i]["История"])):
            driversList[i]["История"][g] = driversListCopy[i]["История"][g].copy()


def AddBuses():
    print("Введите id: ", end="")
    id = input()
    for i in range(len(busList)):
        while (busList[i]["id"] == id):
            print("Такой id автобуса уже существует, введите другой id: ", end="")
            id = input()
    RewriteCopy()
    print("Введите Гос.номер: ", end="")
    number = input()
    print("Введите маршрут: ", end="")
    route = input()
    print("Введите дату ТО")
    todate = StrCheckDate()
    busDownDict["id"] = id
    busDownDict["Гос. номер"] = number
    busDownDict["Маршрут"] = route
    busDownDict["Дата ТО"] = todate
    busList.append(busDownDict.copy())
    busDict["Автобусы"] = busList
    print("Автобус добавлен\n")


def DelBuses():
    print("Введите id автобуса, который хотите удалить: ", end="")
    id = input()
    tempIdList = list()
    for i in range(len(busList)):
        tempIdList.append(busList[i]["id"])
    if id in tempIdList:
        RewriteCopy()
        for i in range(len(busList)):
            if busList[i]["id"] == id:
                busList.remove(busList[i])
                index = id
                print(f"Автобус с id {id} удален\n")
                break
        for i in range(len(driversList)):
            for g in range(len(driversList[i]["История"])):
                if driversList[i]["История"][g]["id"] == index:
                    driversList[i]["История"].remove(driversList[i]["История"][g])
    elif not id in tempIdList:
        print(f"id автобуса {idFind} не найден\n")


def AddDrivers():
    driversDownList = list()
    driversDownDict = dict()
    driversDownDownDict = dict()
    print("Введите ФИО водителя, которого хотите добавить: ", end="")
    fio = input()
    for i in range(len(driversList)):
        if driversList[i]["ФИО"] == fio:
            print("Водитель с таким же ФИО уже есть в списке\n", end = "")
            return
    driversDownDict["ФИО"] = fio
    print("Введите id автобуса: ", end="")
    id = input()
    tempListId = list()
    for i in range(len(busList)):
        tempListId.append(busList[i]["id"])
    if id not in tempListId:
        print(f"id автобуса {id} не найден\n")
        return
    RewriteCopy()
    print("Введите дату выезда")
    dateDep = StrCheckDate()
    print("Введите дату сдачи смены")
    datePas = StrCheckDate()
    driversDownDownDict["id"] = id
    driversDownDownDict["Дата выезда"] = dateDep
    driversDownDownDict["Дата сдачи смены"] = datePas
    driversDownList.append(driversDownDownDict)
    driversDownDict["История"] = driversDownList
    driversList.append(driversDownDict)
    driversDict["Водители"] = driversList
    print("Водитель добавлен\n")

def AddStory():
    if len(busList) == 0:
        print("Сначала нужно добавить автобусы!\n")
        return
    print("Введите ФИО водителя, в историю которого вы хотите добавить запись: ", end = "")
    fio = input()
    isFind = False
    for i in range(len(driversList)):
        if driversList[i]["ФИО"] == fio:
            index = i
            isFind = True
            break
    if isFind:
        print("Введите id автобуса: ", end = "")
        id = input()
        tempListId = list()
        for i in range(len(busList)):
            tempListId.append(busList[i]["id"])
        if id not in tempListId:
            print(f"Автобус с id {id} не найден\n")
            return
        RewriteCopy()
        print("Введите дату выезда")
        dateDep = StrCheckDate()
        print("Введите дату сдачи смены")
        datePas = StrCheckDate()
        dateDict = dict()
        dateDict["id"] = id
        dateDict["Дата выезда"] = dateDep
        dateDict["Дата сдачи смены"] = datePas
        driversList[index]["История"].append(dateDict)
        print("История добавлена\n")
    else:
        print(f"ФИО {fio} не найдено\n")

def DelStory():
    print("Введите ФИО водителя, историю которого вы хотите удалить: ", end = "")
    fio = input()
    isFind = False
    for i in range(len(driversList)):
        if driversList[i]["ФИО"] == fio:
            index = i
            isFind = True
            break
    if isFind:
        print("Введите id автобуса, данные о котором вы хотите удалить: ", end = "")
        id = input()
        tempListId = list()
        if len(driversList[index]["История"]) != 0:
            for g in range(len(driversList[index]["История"])):
                tempListId.append(driversList[index]["История"][g]["id"])
        if id not in tempListId:
            print(f"id автобуса {id} в истории водителя не найден\n")
        else:
            RewriteCopy()
            for i in range(len(driversList[index]["История"])-1, -1, -1):
                if driversList[index]["История"][i]["id"] == id:
                    driversList[index]["История"].remove(driversList[index]["История"][i])
                    break
            print(f"История {fio} по автобусу с id {id} удалена\n")
    else:
        print("ФИО не найдено\n")

def DelDrivers():
    print("Введите ФИО водителя, которого хотите удалить: ", end="")
    fio = input()
    isDel = False
    tempFioList = list()
    for i in range(len(driversList)):
        tempFioList.append(driversList[i]["ФИО"])
    if not fio in tempFioList:
        print(f"Водитель с фио {fio} не найден\n")
    else:
        RewriteCopy()
        for i in range(len(driversList)):
            if driversList[i]["ФИО"] == fio:
                driversList.remove(driversList[i])
                isDel = True
                print("Удаление произведено\n")
                break


def ChangeBuses():
    if len(busList) == 0:
        print("Сначала нужно добавить автобусы!\n")
        return
    print("Введите id автобуса, данные которого вы хотите изменить: ", end="")
    id = input()
    isFind = False
    for i in range(len(busList)):
        if busList[i]["id"] == id:
            isFind = True
            index = i
            break
    if not isFind:
        print("Автобус с таким id не найден\n")
    else:
        RewriteCopy()
        print("Введите, что вы хотите изменить\n"
              "1. id\n"
              "2. Гос. номер\n"
              "3. Маршрут\n"
              "4. Дату ТО")
        answer = input()
        while answer != "1" and answer != "2" and answer != "3" and answer != "4":
            print("Введите число от 1 до 4: ", end = "")
            answer = input()
        if answer == "1":
            print("Введите новое id: ", end="")
            Newid = input()
            for i in range(len(busList)):
                while busList[i]["id"] == Newid:
                    print("Такое id уже существует, введите другое id: ", end="")
                    Newid = input()
            busList[index]["id"] = Newid
            ChangeBusIdInDrivers(id, Newid)
            print("id изменено\n")
        if answer == "2":
            print("Введите новый гос. номер: ", end="")
            number = input()
            busList[index]["Гос. номер"] = number
            print("Гос. номер изменён\n")
        if answer == "3":
            print("Введите новый маршрут: ", end="")
            route = input()
            busList[index]["Маршрут"] = route
            print("Маршрут изменён\n")
        if answer == "4":
            print("Введите новую дату ТО")
            date = StrCheckDate()
            busList[index]["Дата ТО"] = date
            print("Дата ТО изменена\n")

def ChangeBusIdInDrivers(oldId, newId):
    for i in range(len(driversList)):
        for g in range(len(driversList[i]["История"])):
            if driversList[i]["История"][g]["id"] == oldId:
                driversList[i]["История"][g]["id"] = newId


def ChangeDrivers():
    print("Введите ФИО водителя, поля которого вы хотите изменить: ", end = "")
    fio = input()
    tempDrivers = list()
    for i in range(len(driversList)):
        tempDrivers.append(driversList[i]["ФИО"])
    if not fio in tempDrivers:
        print("Водитель с таким ФИО не найден\n")
        return
    else:
        index = tempDrivers.index(fio)
        print("Введите, что вы хотите изменить?\n1. ФИО\n2. Историю")
        answer = input()
        while answer != "1" and answer != "2":
            print("Введите либо 1, либо 2: ", end = "")
            answer = input()
        if answer == "1":
            RewriteCopy()
            print(f"Введите, на какое ФИО вы хотите изменить {fio}: ", end = "")
            newFio = input()
            while newFio in tempDrivers:
                print("Такое фио уже есть в списке водителей. Введите другое ФИО: ", end = "")
                newFio = input()
            driversList[index]["ФИО"] = newFio
            print("ФИО изменено\n")
        else:
            print(f"Историю по автобусу с каким id вы хотите изменить у {fio}: ", end = "")
            answer = input()
            tempIdList = list()
            for i in range(len(driversList[index]["История"])):
                tempIdList.append(driversList[index]["История"][i]["id"])
            if answer in tempIdList:
                indexId = len(tempIdList) - 1 - tempIdList[::-1].index(answer)
                print("Введите, какое поле вы хотите изменить?\n1. id\n2. Дата выезда\n3. Дата сдачи смены")
                answer = input()
                while not answer == "1" and answer != "2" and answer != "3":
                    print("Введите число от 1 до 3")
                    answer = input()
                if answer == "1":
                    print("Введите новое id: ", end = "")
                    answer = input()
                    tempBusid = list()
                    for i in range(len(busList)):
                        tempBusid.append(busList[i]["id"])
                    if not answer in tempBusid:
                        print("Такого id автобуса не существует\n")
                        return
                    RewriteCopy()
                    driversList[index]["История"][indexId]["id"] = answer
                    print("id изменено\n")
                    return
                if answer == "2":
                    RewriteCopy()
                    print("Введите новую дату выезда")
                    date = StrCheckDate()
                    driversList[index]["История"][indexId]["Дата выезда"] = date
                    return
                if answer == "3":
                    RewriteCopy()
                    print("Введите новую дату сдачи смены")
                    date = StrCheckDate()
                    driversList[index]["История"][indexId]["Дата сдачи смены"] = date
                    return
            else:
                print(f"История по автобусу с id {answer} не найдена\n")


def PrintDriverStory():
    print("Введите ФИО водителя, историю которого вы хотите вывести: ", end = "")
    fio = input()
    tempfioList = list()
    for i in range(len(driversList)):
        tempfioList.append(driversList[i]["ФИО"])
    if not fio in tempfioList:
        print("Нет водителя с таким ФИО\n")
    else:
        index = tempfioList.index(fio)
        if len(driversList[index]["История"]) != 0:
            for i in range(len(driversList[index]["История"])):
                isPrint = False
                if len(busList) != 0:
                    for g in range(len(busList)):
                        if (busList[g]["id"] == driversList[index]["История"][i]["id"]):
                            print(str(i + 1) + ".\n" + f"id: {busList[g]['id']}\n"
                            f"Гос. номер: {busList[g]['Гос. номер']}\n"
                            f"Маршрут: {busList[g]['Маршрут']}\n"
                            f"Дата ТО: {busList[g]['Дата ТО']}\n"
                            f"Дата выезда: {driversList[index]['История'][i]['Дата выезда']}\n"
                            f"Дата сдачи смены: {driversList[index]['История'][i]['Дата сдачи смены']}\n")
                            isPrint = True
                            break
        else:
            print(f"Истории водителя с ФИО {fio} нет\n")

answer = "133"
while answer != "0":
    print("Введите, что вы хотите сделать?\n"
          "1. Добавить автобус\n"
          "2. Удалить автобус\n"
          "3. Добавить водителя\n"
          "4. Удалить водителя\n"
          "5. Добавить историю\n"
          "6. Удалить историю\n"
          "7. Изменить поля автобуса\n"
          "8. Изменить поля водителя\n"
          "9. Вывести на печать\n"
          "10. Вывести на печать полную историю водителя\n"
          "11. Вывести на печать только автобусы\n"
          "12. Вывести на печать только водителей\n"
          "13. Отменить последние изменение\n"
          "0. Выход")

    answer = input()

    while answer != "1" and answer != "2" and answer != "3" and answer != "4" and answer != "5" and \
            answer != "6" and answer != "7" and answer != "8" and answer != "9" and answer != "10" and\
            answer != "11" and answer != "12" and answer != "13" and  answer != "0":
        print("Введите число от 0 до 13!")
        answer = input()
    if answer == "0":
        print("Благодарим за использование программы")
        break
    if answer == "1":
        AddBuses()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "2":
        DelBuses()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "3":
        if len(busList) == 0:
            print("Сначало нужно добавить автобусы\n")
        else:
            AddDrivers()
            busDict.update(driversDict)
            try:
                f = open("busPark.json", "w")
                f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
                f.close()
            except BaseException:
                print("Ошибка работы с файлом busPark.json\n")
    elif answer == "4":
        DelDrivers()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "5":
        AddStory()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "6":
        DelStory()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "7":
        ChangeBuses()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "8":
        ChangeDrivers()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "9":
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w+")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
            with open("busPark.json", "r") as readfile:
                pr = readfile.read()
                json.loads(pr)
                print(pr)
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "10":
        PrintDriverStory()
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w+")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")
    elif answer == "11":
        if len(busList) == 0:
            print("Автобусов нет\n")
        else:
            print("Автобусы:\n")
            for i in range(len(busList)):
                print(str(i+1) + ".")
                if busList[i]["id"] == "":
                    print('id: ""')
                else:
                    print("id: " + busList[i]["id"])
                if busList[i]["Гос. номер"] == "":
                    print('Гос. номер: ""')
                else:
                    print("Гос. номер: " + busList[i]["Гос. номер"])
                print("Дата ТО: " + busList[i]["Дата ТО"])
                if busList[i]["Маршрут"] == "":
                    print('Маршрут: ""\n')
                else:
                    print("Маршрут: " + busList[i]["Маршрут"] + "\n")
    elif answer == "12":
        if len(driversList) == 0:
            print("Водителей нет\n")
        else:
            print("Водители:\n")
            for i in range(len(driversList)):
                print(str(i+1) + ".")
                if driversList[i]["ФИО"] == "":
                    print('ФИО: ""')
                else:
                    print("ФИО: " + driversList[i]["ФИО"])
                if len(driversList[i]["История"]) == "":
                    print('История: ""')
                else:
                    print("История:")
                for g in range(len(driversList[i]["История"])):
                    print("\t" + str(g+1) + ".")
                    if driversList[i]["История"][g]["id"] == "":
                        print('\tid: ""')
                    else:
                        print("\tid: " + driversList[i]["История"][g]["id"])
                    print("\tДата выезда: " + driversList[i]["История"][g]["Дата выезда"])
                    print("\tДата сдачи смены: " + driversList[i]["История"][g]["Дата сдачи смены"] + "\n")
    elif answer == "13":
        RewriteMain()
        busDict["Автобусы"] = busList
        driversDict["Водители"] = driversList
        busDict.update(driversDict)
        try:
            f = open("busPark.json", "w+")
            f.write(json.dumps(busDict, ensure_ascii=False, indent=4))
            f.close()
            print("Последнее изменение отменено\n")
        except BaseException:
            print("Ошибка работы с файлом busPark.json\n")


