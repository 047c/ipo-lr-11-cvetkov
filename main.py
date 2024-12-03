import transport

decor = "=" * 22
Status = True
all_clients = []
all_vehicles = []
all_company = []


def double_decor():
    print(f"{decor}{decor}")


def print_menu():
    print(f"{decor} Меню {decor}")
    print(f"1 - Создать клиента")
    print(f"2 - Управлять транспортом")
    print(f"3 - Управлять компаниями")
    print(f"4 - Вывести информацию о всех клиентах")
    print(f"5 - Вывести информацию о всех транспортах")
    print(f"6 - Вывести информацию о всех компаниях")
    print(f"7 - Завершить выполнение программы")


def print_vehicle_menu():
    print(f"{decor} Управлять транспортом {decor}")
    print(f"1 - Создать грузовик")
    print(f"2 - Создать лодку")
    print(f"3 - Загрузить груз клиента в транспорт")


def print_company_menu():
    print(f"{decor} Управлять компаниями {decor}")
    print(f"1 - Создать компанию")
    print(f"2 - Добавить транспортное средство в компанию")
    print(f"3 - Список всех транспортных средств компании")
    print(f"4 - Добавить клиента в компанию")
    print(f"5 - Распределить грузы клиентов по транспортным средствам")


while Status:
    print_menu()
    double_decor()
    input_data = input("Введите номер: ")
    double_decor()
    try:
        input_data = int(input_data)
    except ValueError:
        print("Введите корректное значение!")
    if input_data == 1:
        name = input("Введите имя нового клиента: ")
        cargo = input("Введите вес груза нового клиента: ")
        is_vip = input("Укажите является ли новый клиент вип персоной? Отправьте 1, если это так, а если это не так, "
                       "то отправьте любое значение: ")
        is_vip = True if is_vip == "1" else False
        try:
            cargo = int(cargo)
            all_clients.append(transport.Client(name, cargo, is_vip))
            print("Новый клиент был успешно создан!")
        except:
            print("Введите корректное значение веса груза нового клиента!")
    elif input_data == 2:
        print_vehicle_menu()
        double_decor()
        input_data = input("Введите номер: ")
        double_decor()
        try:
            input_data = int(input_data)
        except ValueError:
            print("Введите корректное значение!")
        if input_data == 1:
            capacity = input("Введите грузоподъёмность грузовика: ")
            is_refrigerated = input(
                "Укажите, есть ли у грузовика холодильник? Отправьте 1, если это так, а если это не так, "
                "то отправьте любое значение: ")
            is_refrigerated = True if is_refrigerated == "1" else False
            try:
                capacity = int(capacity)
                all_vehicles.append(transport.Van(capacity, is_refrigerated))
                print("Грузовик создан!")
            except:
                print("Введите корректное значение грузоподъёмности!")
        elif input_data == 2:
            capacity = input("Введите грузоподъёмность судна: ")
            name = input("Введите название судна: ")
            try:
                capacity = int(capacity)
                all_vehicles.append(transport.Ship(capacity, name))
                print("Лодка создана!")
            except ValueError:
                print("Введите корректное значение грузоподъёмности!")
        elif input_data == 3:
            target_vehicle = input("Введите номер транспорта, в который хотите загрузить груз: ")
            target_client = input("Введите номер клиента, груз которого хотите загрузить: ")
            try:
                target_client = int(target_client)
                target_vehicle = int(target_vehicle)
                all_vehicles[target_vehicle - 1].load_cargo(all_clients[target_client - 1])
                print("Успешно выполнено!")
            except:
                print("Возникла ошибка! Проверьте корректность введенных данных!")
    elif input_data == 3:
        print_company_menu()
        input_data = input("Введите номер: ")
        double_decor()
        try:
            input_data = int(input_data)
        except ValueError:
            print("Введите корректное значение!")
        if input_data == 1:
            name = input("Введите название компании: ")
            vehicles = []
            clients = []
            all_company.append(transport.TransportCompany(name, vehicles, clients))
            print("Компания успешно создана!")
        elif input_data == 2:
            target_vehicle = input("Введите номер транспорта, который хотите добавить в компанию: ")
            target_company = input("Введите номер компании, к которой хотите добавить транспорт: ")
            try:
                target_company = int(target_company)
                target_vehicle = int(target_vehicle)
                all_company[target_company - 1].add_vehicle(all_vehicles[target_vehicle - 1])
                print("Успешно добавлено!")
            except:
                print("Произошла ошибка! Проверьте корректность введенных данных!")
        elif input_data == 3:
            target_company = input("Введите номер компании, список транспорта которой Вы хотите посмотреть: ")
            try:
                target_company = int(target_company)
                double_decor()
                print(f"Вот список транспорта компании с идентификатором {target_company}:")
                target_company -= 1
                id = 0
                for vehicle in all_company[target_company].vehicles:
                    id += 1
                    print(
                        f"{id}. Уникальный идентификатор транспорта: {vehicle.vehicle_id}. Грузоподъёмность: {vehicle.capacity}. Сейчас загружено: {vehicle.current_load}. Список клиентов: ",
                        end="")
                    for client in vehicle.clients_list:
                        print(client.name, end=" ")
            except ValueError:
                print("Введите корректное значение!")
            print()
        elif input_data == 4:
            target_company = input("Введите номер компании, куда хотите добавить клиента: ")
            target_client = input("Введите номер клиента, которого хотите добавить в компанию: ")
            try:
                target_company = int(target_company)
                target_client = int(target_client)
                all_company[target_company - 1].add_client(all_clients[target_client - 1])
                print("Успешно добавлено!")
            except ValueError:
                print("Введите корректное значение!")
        elif input_data == 5:
            target_company = input("Введите номер компании, где хотите распределить груз: ")
            try:
                target_company = int(target_company)
                all_company[target_company - 1].optimize_cargo_distribution()
            except ValueError:
                print("Введите корректное значение номера компании!")
    elif input_data == 4:
        id = 0
        for client in all_clients:
            id += 1
            vip = "Да" if client.is_vip else "Нет"
            print(f"{id}. Имя: {client.name}. Вес груза: {client.cargo_weight}. VIP-статус: {vip}")
    elif input_data == 5:
        id_number = 0
        for vehicle in all_vehicles:
            id_number += 1
            print(
                f"{id_number}. Уникальный идентификатор транспорта: {vehicle.vehicle_id}. Грузоподъёмность: {vehicle.capacity}. Сейчас загружено: {vehicle.current_load}. Список клиентов: ", end="")
            for client in vehicle.clients_list:
                print(client.name, end=" ")
        print()
    elif input_data == 6:
        id = 0
        for company in all_company:
            id += 1
            print(f"{id}. Название компании: {company.name}")
            print(f"| Список транспортных средств: ")
            for vehicle in company.vehicles:
                print(
                    f"| Уникальный идентификатор транспорта: {vehicle.vehicle_id}. Грузоподъёмность: {vehicle.capacity}. Сейчас загружено: {vehicle.current_load}. Список клиентов: ")
                for client in vehicle.clients_list:
                    print(f"| {client.name}")
            print(f"| Список клиентов компании: ")
            for client in company.clients:
                vip = "Да" if client.is_vip else "Нет"
                print(f"| Имя клиента: {client.name}. Вес груза: {client.cargo_weight}. VIP-статус: {vip}")
    elif input_data == 7:
        Status = False
        print("Завершаю выполнение программы...")
