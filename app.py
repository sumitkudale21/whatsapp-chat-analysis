class car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        
    def get_info(self):
        return f"Make: {self.make}, Model: {self.model}, Year: {self.year}"
    
car1 = car('toyota','fortuner',2020)
print(car1.get_info())