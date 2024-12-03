class TransportCompany():
    def __init__(self, name, vehicles, clients):
        self.name = name
        if not isinstance(vehicles, list):
            raise AttributeError("Аттрибут vehicles должен быть списком")
        if not isinstance(clients, list):
            raise AttributeError("Аттрибут clients должен быть списком")
        self.name = name
        self.vehicles = vehicles
        self.clients = clients
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    def list_vehicles(self):
        return self.vehicles
    def add_client(self, client):
        self.clients.append(client)
    def optimize_cargo_distribution(self):
        priority = []
        not_priority = []
        success = []
        for self_client in self.clients:
            if self_client.is_vip:
                priority.append(self_client)
        for self_client in self.clients:
            if self_client not in priority:
                not_priority.append(self_client)
        for self_client in priority:
            for vehicle in self.vehicles:
                free_space = vehicle.capacity - vehicle.current_load
                weight = self_client.cargo_weight
                if free_space >= weight:
                    vehicle.current_load += weight
                    vehicle.clients_list.append(self_client)
                    success.append(self_client)
                    break
        for self_client in not_priority:
            for vehicle in self.vehicles:
                free_space = vehicle.capacity - vehicle.current_load
                weight = self_client.cargo_weight
                if free_space >= weight:
                    vehicle.current_load += weight
                    vehicle.clients_list.append(self_client)
                    success.append(self_client)
                    break
        print("Груз успешно оптимизирован и распределен для следующих клиентов компании:", end=" ")
        for clients in success:
            print(f"{clients.name}", end=" ")
        print()
