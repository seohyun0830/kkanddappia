class FuelManager:
    def __init__(self):
        self.fuel = 80          
        self.max_fuel = 100

    def set_fuel(self, amount):
        self.fuel = max(0, min(amount, self.max_fuel))

    def add_fuel(self, amount):
        self.fuel = min(self.fuel + amount, self.max_fuel)

    def consume_fuel(self, amount):
        self.fuel = max(0, self.fuel - amount)

# ------------ 전역 싱글톤 객체 ------------ #
fuel_manager = FuelManager()
