class Client():
    def __init__(self, name, cargo_weight, is_vip=False):
        if name:
            self.name = name
        else:
            raise ValueError("Имя должно быть указано!")
        try:
            cargo_weight = int(cargo_weight)
            self.cargo_weight = cargo_weight
        except ValueError:
            raise ValueError("Вес груза должен быть обязательно указан числом")
        if not (is_vip == True or is_vip == False):
            raise ValueError("Флаг вип статуса указывается bool типом")
        self.is_vip = bool(is_vip)