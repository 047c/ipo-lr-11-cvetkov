import random
class Vehicle():
    def __init__(self, capacity, current_load=0):
        self.vehicle_id = str(random.randint(1000, 100000))
        try:
            capacity = int(capacity)
        except ValueError:
            raise ValueError("Груподоъемность указывается числом")
        try:
            current_load = int(current_load)
        except ValueError:
            raise ValueError("Текущая загрузка указывается числом")
        self.capacity = capacity
        self.clients_list = []
        self.current_load = current_load
    def load_cargo(self, client):
        try:
            new_weight = self.current_load + client.cargo_weight
        except AttributeError:
            raise AttributeError("Вы должны передать клиента в параметр функции!")
        if new_weight > self.capacity:
            print("Грузоподъемность превышена! Действие отменено!")
        else:
            self.current_load = new_weight
            self.clients_list.append(client)
    def str(self):
        return f"ID транспорта: {self.vehicle_id}\n Грузоподъемность транспорта: {self.capacity}\n Загружено: {self.current_load}"