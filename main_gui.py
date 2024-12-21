import dearpygui.dearpygui as dpg
import transport

global ERROR_TEXT, ERROR_CODE, TABLE_CLIENT, TABLE_TRANSPORT, TABLE_STATUS

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1650, height=800, resizable=False)

all_clients = []
all_vehicles = []
all_company = []
all_logs = []
last_cargo = []


def _button(sender, user_data):
    global ERROR_TEXT, ERROR_CODE
    pos = dpg.get_mouse_pos()
    if sender == "add_client":
        dpg.configure_item("client_window", pos=pos)
        dpg.show_item("client_window")
    elif sender == "add_transport":
        dpg.configure_item("transport_window", pos=pos)
        dpg.show_item("transport_window")
    elif sender == "create_client":
        client_name = dpg.get_value("client_name")
        client_cargo = dpg.get_value("client_cargo")
        client_vip = dpg.get_value("client_vip")
        length = len(client_name)
        if length < 2 or length >= 64:
            dpg.set_value("client_name", "")
            ErrorModal("Длина имени клиента должна быть больше 2 и меньше 64!")
        elif client_cargo < 0 or client_cargo > 10000:
            dpg.set_value("client_cargo", 0)
            ErrorModal("Вес груза должен быть больше 0 и меньше 10000!")
        else:
            #SuccessModal("Клиент создан!")
            all_clients.append(transport.Client(client_name, client_cargo, client_vip))
            addLog(f"Создан клиент. Таблица обновлена")
            relLogs()
            relClient()
    elif sender == "t_save":
        capacity = dpg.get_value("t_capacity")
        is_refrigerated = dpg.get_value("is_refrigerated")
        if capacity < 0 or capacity > 10000:
            dpg.set_value("t_capacity", 0)
            ErrorModal("Вес груза должен быть больше 0 и меньше 10000!")
        else:
            #SuccessModal("Фургон создан!")
            addLog(f"Создан фургон. Таблица обновлена")
            relLogs()
            all_vehicles.append(transport.Van(capacity, is_refrigerated))
            relTransport()
    elif sender == "t_save2":
        capacity = dpg.get_value("t_capacity")
        name = dpg.get_value("t_name")
        if capacity < 0 or capacity > 10000:
            dpg.set_value("t_capacity", 0)
            ErrorModal("Вес груза должен быть больше 0 и меньше 10000!")
        else:
            #SuccessModal("Лодка создана!")
            addLog(f"Создана лодка. Таблица обновлена")
            relLogs()
            all_vehicles.append(transport.Ship(capacity, name))
            relTransport()
    elif sender == "create_company":
        dpg.configure_item("company_window", pos=pos)
        dpg.show_item("company_window")
    elif sender == "c_save":
        name = dpg.get_value("c_name")
        length = len(name)
        if length < 2 or length >= 64:
            dpg.set_value("c_name", "")
            ErrorModal("Длина имени компании должна быть больше 2 и меньше 64!")
        else:
            all_company.append(transport.TransportCompany(name=name, clients=all_clients, vehicles=all_vehicles))
            addLog(f"Создана компания. Таблица обновлена")
            relLogs()
            SuccessModal(f"Компания {name} успешно создана!")
    elif sender == "optimize_cargo":
        dpg.delete_item("OSelect")
        dpg.delete_item("OText")
        dpg.delete_item("OSep")
        dpg.delete_item("modal_group")
        dpg.delete_item("OAbort")
        dpg.configure_item("__popup_optimize", pos=pos)
        dpg.add_combo(returnCompanies(), default_value="Нажмите, чтобы раскрыть", tag="OSelect", parent="__popup_optimize")
        dpg.add_text("Это действие невозможно отменить!", tag="OText", parent="__popup_optimize")
        dpg.add_separator(tag="OSep", parent="__popup_optimize")
        dpg.add_group(horizontal=True, tag="modal_group", parent="__popup_optimize")
        dpg.add_button(label="Да", width=75, tag="run_optimize", callback=_button, parent="modal_group")
        dpg.add_button(label="Нет", width=75, parent="modal_group",
                       tag="OAbort", callback=lambda: dpg.configure_item("__popup_optimize", show=False))
        dpg.show_item("__popup_optimize")
    elif sender == "run_optimize":
        dpg.hide_item("__popup_optimize")
        value = dpg.get_value("OSelect")
        for company in all_company:
            if company.name == value:
                success = company.optimize_cargo_distribution()
                if dpg.does_item_exist("cargo_results"):
                    dpg.delete_item("cargo_results")
                if dpg.does_item_exist("cAbort"):
                    dpg.delete_item("cAbort")
                if dpg.does_item_exist("cOk"):
                    dpg.delete_item("cOk")
                dpg.set_value("cargo_success_text", f"Последнее распределение грузов для компании {company.name}")
                table = dpg.add_table(resizable=True, sortable=True, row_background=True, parent="__popup_cargo_result",
                                      tag="cargo_results", scrollX=True, scrollY=True)
                dpg.add_table_column(label="Клиенты, грузы которых были распределены: ", parent=table)
                CLIENT_TARGET = 0
                for client in success:
                    CLIENT_TARGET += 1
                    vip_status = "Есть" if client.is_vip is True else "Нет"
                    TARGET_ROW = f"cargo_{CLIENT_TARGET}"
                    dpg.add_table_row(tag=TARGET_ROW, parent=table)
                    dpg.add_selectable(
                        label=f"{CLIENT_TARGET}. Имя: {client.name}. Вес груза: {client.cargo_weight}. VIP: {vip_status}",
                        span_columns=True,
                        callback=on_table_row_double_click, parent=TARGET_ROW, user_data=f"cargo_{CLIENT_TARGET}")
                dpg.add_separator(tag="cOk", parent="__popup_cargo_result")
                dpg.add_button(label="Ок", width=75, parent="__popup_cargo_result",
                               callback=lambda: dpg.configure_item("__popup_cargo_result", show=False))
                last_cargo.append(success.copy())
                addLog(f"Грузы оптимизированы. Результат отображен на экран и записан как последний.")
                relLogs()
def SaveThis(sender, app_data, sender_data):
    target = f"capacity_{sender_data}"
    capacity = dpg.get_value(target)
    if capacity < 0 or capacity > 10000:
        dpg.set_value(target, 0)
        ErrorModal("Вес груза должен быть больше 0 и меньше 10000!")
    else:
        if sender_data[:2] == "cl":
            target = f"name_{sender_data}"
            name = dpg.get_value(target)
            length = len(name)
            if length < 2 or length >= 64:
                dpg.set_value(target, "")
                ErrorModal("Длина имени клиента должна быть больше 2 и меньше 64!")
            else:
                try:
                    number_of_object = sender_data[3:]
                    number_of_object = int(number_of_object)
                    number_of_object -= 1
                    all_clients[number_of_object].cargo_weight = capacity
                    all_clients[number_of_object].name = name
                    SuccessModal("Клиент успешно отредактирован!")
                    relClient()
                    addLog("Отредактирован клиент. Таблица обновлена")
                    relLogs()
                except:
                    ErrorModal("Ошибка! Проверьте корректность введенных данных")
        elif sender_data[:2] == "ts":
            try:
                number_of_object = sender_data[3:]
                number_of_object = int(number_of_object)
                number_of_object -= 1
                all_vehicles[number_of_object].capacity = capacity
                SuccessModal("Транспорт успешно отредактирован!")
                relTransport()
                addLog("Отредактирован транспорт. Таблица обновлена")
                relLogs()
            except:
                ErrorModal("Ошибка! Проверьте корректность введенных данных")

def DeleteThis(sender, app_data, sender_data):
    number_of_object = sender_data[3:]
    number_of_object = int(number_of_object)
    number_of_object -= 1
    window = f"window_{sender_data}"
    if sender_data[:2] == "cl":
        try:
            all_clients.pop(number_of_object)
            dpg.delete_item(window)
            SuccessModal("Клиент успешно удален!")
            addLog("Клиент удален. Таблица обновлена")
            relClient()
            relLogs()
        except:
            ErrorModal("Ошибка! Проверьте корректность введенных данных")
    elif sender_data[:2] == "ts":
        try:
            all_vehicles.pop(number_of_object)
            dpg.delete_item(window)
            SuccessModal("Транспорт успешно удален!")
            addLog("Транспорт удален. Таблица обновлена")
            relTransport()
            relLogs()
        except:
            ErrorModal("Ошибка! Проверьте корректность введенных данных")

def on_table_row_double_click(sender, app_data, sender_data):
    if app_data is True:
        pos = dpg.get_mouse_pos()
        target = f"window_{sender_data}"
        if sender_data[:2] == "ts":
            dpg.add_window(label="Изменить транспорт", tag=target, show=False, width=400, height=250)
            dpg.add_text("Грузоподъёмность", parent=target)
        elif sender_data[:2] == "cl":
            dpg.add_window(label="Изменить клиента", tag=target, show=False, width=400, height=250)
            dpg.add_text("Имя клиента", parent=target)
            dpg.add_input_text(tag=f"name_{sender_data}", parent=target)
            dpg.add_text("Вес груза в тоннах", parent=target)
        dpg.add_input_float(tag=f"capacity_{sender_data}", min_value=0, max_value=99999, default_value=0,
                            parent=target)
        group = f"group_{sender_data}"
        dpg.add_group(horizontal=True, parent=target, tag=group)
        dpg.add_button(label="Изменить", callback=SaveThis, user_data=sender_data, parent=group)
        dpg.add_button(label="Удалить", callback=DeleteThis, user_data=sender_data, parent=group)
        dpg.configure_item(target, pos=(pos[0], pos[1]))
        dpg.show_item(target)
    elif app_data is False:
        dpg.delete_item(f"window_{sender_data}")


def returnCompanies():
    returned = list()
    for company in all_company:
        returned.append(company.name)
    return returned

with dpg.handler_registry():
    dpg.add_mouse_double_click_handler(callback=on_table_row_double_click)

def exportResult():
    if len(all_clients) == 0 and len(all_vehicles) == 0 and len(all_company) == 0:
        ErrorModal("Невозможно экспортировать результат: данные отсутствуют")
    else:
        with open("data.txt", "w", encoding="utf-8") as file:
            file.write("Клиенты:\n")
            for client in all_clients:
                file.write(f"Имя: {client.name}, вес груза: {client.cargo_weight}\n")
            file.write("Транспорт:\n")
            for vehicle in all_vehicles:
                file.write(f"ID: {vehicle.vehicle_id}, грузоподъёмность: {vehicle.capacity}\n")
            file.write("Компании:\n")
            for company in all_company:
                file.write(f"Название компании: {company.name}")
    SuccessModal("Результат успешно экспортирован в data.txt файл!")

def exportOptimize():
    if len(last_cargo) == 0:
        ErrorModal("Невозможно экспортировать результат: данные отсутствуют")
    else:
        with open("cargo.txt", "w", encoding="utf-8") as file:
            counter = 0
            for cargo in last_cargo:
                counter += 1
                file.write(f"Распределение {counter}. Успешное распределение для: \n")
                for client in cargo:
                    file.write(f"Имя: {client.name}, вес груза: {client.cargo_weight}\n")
    SuccessModal("Результат успешно экспортирован в cargo.txt файл!")

def _checkbox(sender, user_data):
    pass


def create_button(tag, label="", user_data=None, arrow=False):
    return dpg.add_button(tag=tag, arrow=arrow, label=label, callback=_button, user_data=user_data)


def create_checkbox(tag, label="", user_data=None):
    return dpg.add_checkbox(tag=tag, label=label, callback=_checkbox, user_data=user_data)


def ErrorModal(ERROR_TEXT="Ошибка"):
    dpg.configure_item("__popup_error", pos=dpg.get_mouse_pos(), width=400, height=150)
    dpg.set_value("ERROR_TEXT", ERROR_TEXT)
    dpg.show_item("__popup_error")

def SuccessModal(SUCCESS_TEXT="Успех"):
    dpg.configure_item("__popup_success", pos=dpg.get_mouse_pos(), width=400, height=150)
    dpg.set_value("SUCCESS_TEXT", SUCCESS_TEXT)
    dpg.show_item("__popup_success")

def initCargoResult ():
    dpg.configure_item("__popup_cargo_result", pos=dpg.get_mouse_pos())
    dpg.show_item("__popup_cargo_result")
def TransportType(sender):
    window_tag = "transport_window"
    value = dpg.get_value(sender)
    dpg.hide_item("t_text1")
    dpg.hide_item("t_text2")
    dpg.hide_item("t_capacity")
    dpg.hide_item("is_refrigerated")
    dpg.hide_item("t_save")
    dpg.hide_item("t_abort")
    dpg.hide_item("t_name")
    dpg.hide_item("t_text3")
    dpg.hide_item("t_save2")
    dpg.hide_item("t_abort2")
    if value == "Фургон (Van)":
        dpg.show_item("t_text1")
        dpg.show_item("t_text2")
        dpg.show_item("t_capacity")
        dpg.show_item("is_refrigerated")
        dpg.show_item("t_save")
        dpg.show_item("t_abort")
    elif value == "Лодка (Ship)":
        dpg.show_item("t_text1")
        dpg.show_item("t_text3")
        dpg.show_item("t_capacity")
        dpg.show_item("t_save2")
        dpg.show_item("t_abort2")
        dpg.show_item("t_name")

def addLog(text):
    all_logs.append(text)

with dpg.font_registry():
    with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font("Default font")

with dpg.window(label="Добавить клиента", tag="client_window", width=400, height=250, show=False):
    dpg.add_text("Имя клиента")
    dpg.add_input_text(tag="client_name")
    dpg.add_text("Вес груза в тоннах")
    dpg.add_input_float(tag="client_cargo", min_value=0, max_value=10000, default_value=0)
    dpg.add_text("Привилегии")
    create_checkbox(tag="client_vip", label="VIP")
    dpg.add_text("Действие")
    with dpg.group(horizontal=True):
        create_button(tag="create_client", label="Сохранить")
        dpg.add_button(label="Отмена", callback=lambda: dpg.hide_item("client_window"))

with dpg.window(label="Добавить транспорт", tag="transport_window", width=400, height=250, show=False):
    dpg.add_text("Тип транспорта")
    dpg.add_combo(("Фургон (Van)", "Лодка (Ship)"), default_value="Нажмите, чтобы раскрыть", tag="Ttype",
                  callback=TransportType)
    dpg.add_text("Вместимость в тоннах", tag="t_text1", show=False)
    dpg.add_input_float(tag="t_capacity", min_value=0, max_value=99999, default_value=0, show=False)
    dpg.add_text("Особенности", tag="t_text2", show=False)
    dpg.add_checkbox(tag="is_refrigerated", label="Наличие холодильника", callback=_checkbox, show=False)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=_button, tag="t_save", show=False)
        dpg.add_button(label="Отмена", callback=lambda: dpg.hide_item("transport_window"), tag="t_abort", show=False)
    dpg.add_text("Название", tag="t_text3", show=False)
    dpg.add_input_text(tag="t_name", show=False)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=_button, tag="t_save2", show=False)
        dpg.add_button(label="Отмена", callback=lambda: dpg.hide_item("transport_window"), tag="t_abort2", show=False)

with dpg.window(label="Создать компанию", tag="company_window", width=400, height=250, show=False):
    dpg.add_text("Название компании")
    dpg.add_input_text(tag="c_name")
    with dpg.group(horizontal=True):
        create_button(tag="c_save", label="Создать")
        dpg.add_button(label="Отмена", callback=lambda: dpg.hide_item("company_window"))

with dpg.window(label="Распределить грузы!", modal=True, show=False, tag="__popup_optimize", no_title_bar=True):
    dpg.configure_item("__popup_optimize", pos=dpg.get_mouse_pos(), width=400, height=150)
    dpg.add_text("Вы действительно хотите распределить грузы? \n\nВыберите компанию из списка:")
    dpg.add_combo(returnCompanies(), default_value="Нажмите, чтобы раскрыть", tag="OSelect")
    dpg.add_text("Это действие невозможно отменить!", tag="OText")
    dpg.add_separator(tag="OSep")
    with dpg.group(horizontal=True, tag="modal_group"):
        dpg.add_button(label="Да", width=75, tag="run_optimize", callback=_button)
        dpg.add_button(label="Нет", width=75, tag="OAbort", callback=lambda: dpg.configure_item("__popup_optimize",
                                                                                                show=False))

with dpg.window(label="Результаты распределения", modal=True, show=False, tag="__popup_cargo_result"):
    dpg.configure_item("__popup_cargo_result", pos=dpg.get_mouse_pos(), width=400, height=150)
    dpg.add_text(f"Нет информации об последнем распределении грузов", tag="cargo_success_text")
    dpg.add_button(label="Ок", width=75, callback=lambda: dpg.configure_item("__popup_cargo_result", show=False),
                   tag="cAbort")

with dpg.window(label="Внимание!", modal=True, show=False, tag="__popup_error", no_title_bar=True):
    dpg.configure_item("__popup_error", pos=dpg.get_mouse_pos(), width=400, height=150)
    dpg.add_text(f"Возникла ошибка!")
    dpg.add_text("ERROR_TEXT", tag="ERROR_TEXT")
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Ок", width=75, callback=lambda: dpg.configure_item("__popup_error", show=False))

with dpg.window(label="Успех!", modal=True, show=False, tag="__popup_success", no_title_bar=True):
    dpg.add_text(f"Успех!")
    dpg.add_text("SUCCESS_TEXT", tag="SUCCESS_TEXT")
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Ок", width=75, callback=lambda: dpg.configure_item("__popup_success", show=False))

with dpg.window(label="О программе", modal=True, show=False, tag="__popup_info"):
    dpg.add_text(f"Номер лр: 12")
    dpg.add_text(f"Вариант: 3")
    dpg.add_text(f"ФИО: Цветков Владислав Артурович")
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Ок", width=75, callback=lambda: dpg.configure_item("__popup_info", show=False))

def infoModal():
    dpg.show_item("__popup_info")

def relClient():
    if dpg.does_item_exist("preview_clients"):
        dpg.delete_item("preview_clients")
    if dpg.does_item_exist("table_client"):
        dpg.delete_item("table_client")
    table = dpg.add_table(resizable=True, sortable=True, row_background=True, parent="table_clients",
                          tag="table_client", scrollX=True, scrollY=True)
    dpg.add_table_column(label="Существующие клиенты: ", parent=table)
    CLIENT_TARGET = 0
    for client in all_clients:
        CLIENT_TARGET += 1
        vip_status = "Есть" if client.is_vip is True else "Нет"
        TARGET_ROW = f"row_{CLIENT_TARGET}"
        dpg.add_table_row(tag=TARGET_ROW, parent=table)
        dpg.add_selectable(
            label=f"{CLIENT_TARGET}. Имя: {client.name}. Вес груза: {client.cargo_weight}. VIP: {vip_status}",
            span_columns=True,
            callback=on_table_row_double_click, parent=TARGET_ROW, user_data=f"cl_{CLIENT_TARGET}")

def relLogs():
    if dpg.does_item_exist("preview_status"):
        dpg.delete_item("preview_status")
    if dpg.does_item_exist("table_statusbar"):
        dpg.delete_item("table_statusbar")
    table = dpg.add_table(resizable=True, sortable=True, row_background=True, parent="statusbar",
                          tag="table_statusbar")
    dpg.add_table_column(label="Последние действия: ", parent=table)
    LOG_TARGET = 0
    for log in reversed(all_logs):
        LOG_TARGET += 1
        TARGET_ROW = f"lg_{LOG_TARGET}"
        dpg.add_table_row(tag=TARGET_ROW, parent=table)
        dpg.add_selectable(
            label=f"{LOG_TARGET}. {log}",
            span_columns=True, parent=TARGET_ROW)
def relTransport():
    if dpg.does_item_exist("preview_transport"):
        dpg.delete_item("preview_transport")
    if dpg.does_item_exist("table_transport"):
        dpg.delete_item("table_transport")
    table = dpg.add_table(resizable=True, sortable=True, row_background=True, parent="table_transports",
                          tag="table_transport")
    dpg.add_table_column(label="Существующий транспорт: ", parent=table)
    TRANSPORT_TARGET = 0
    for vehicle in all_vehicles:
        TRANSPORT_TARGET += 1
        try:
            is_refrigerated = "Есть" if vehicle.is_refrigerated is True else "Нет"
            type = "Фургон"
        except:
            type = "Лодка"
        TARGET_ROW = f"ts_{TRANSPORT_TARGET}"
        dpg.add_table_row(tag=TARGET_ROW, parent=table)
        dpg.add_selectable(
            label=f"{TRANSPORT_TARGET}. ID: {vehicle.vehicle_id}. Тип: {type}. Грузоподъёмность: {vehicle.capacity}"
                    f". Загруженность: {vehicle.current_load}.",
            span_columns=True,
            callback=on_table_row_double_click, parent=TARGET_ROW, user_data=f"ts_{TRANSPORT_TARGET}")

with dpg.window(tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="Меню"):
            dpg.add_menu_item(label="Экспорт результата", callback=exportResult)
            dpg.add_menu_item(label="Экспорт распределение", callback=exportOptimize)
            dpg.add_menu_item(label="О программе", callback=infoModal)
    with dpg.child_window(autosize_x=True, height=95):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Последнее распределение грузов", width=275, height=75, callback=initCargoResult)
            dpg.add_button(label="Обновить таблицу клиентов", width=275, height=75, callback=relClient)
            dpg.add_button(label="Обновить таблицу транспорта", width=275, height=75, callback=relTransport)
            dpg.add_button(label="Обновить таблицу логов", width=275, height=75, callback=relLogs)
    with dpg.child_window(autosize_x=True, height=175):
        with dpg.group(horizontal=True, width=0):
            with dpg.child_window(width=200, height=150):
                with dpg.tree_node(label="Клиенты"):
                    create_button(label="Добавить клиента", tag="add_client")
                with dpg.tree_node(label="Транспорт"):
                    create_button(label="Добавить транспорт", tag="add_transport")
                    create_button(label="Распределить грузы", tag="optimize_cargo")
                with dpg.tree_node(label="Компании"):
                    create_button(label="Создать компанию", tag="create_company")
            with dpg.child_window(width=700, height=150, tag="table_clients"):
                dpg.add_text("Здесь будут отображаться созданные клиенты", tag="preview_clients")
            with dpg.child_window(width=700, height=150, tag="table_transports"):
                dpg.add_text("Здесь будет отображаться созданный транспорт", tag="preview_transport")
    with dpg.group(horizontal=True):
        with dpg.child_window(autosize_x=True, autosize_y=True, tag="statusbar"):
            dpg.add_text("Здесь будут отображаться текущие действия", tag="preview_status")

dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()