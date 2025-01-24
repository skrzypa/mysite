"""
Sources:
    https://github.com/Brewtarget/brewtarget/blob/develop/src/PrimingDialog.cpp
    https://piwko.com.pl/ 
    https://twojbrowar.pl/pl/blog/jak-zmierzyc-poziom-alkoholu-w-domowym-piwie 

Tested only for glucose
"""



import math
import functools



class BeerCalc():
    def __init__(self, sugar_type: str = 'glucose'):
        self.sugar_types: dict = {
            "glucMono": {"mol_weight": 198, "mol_ratio": 2},
            "glucose": {"mol_weight": 180, "mol_ratio": 2},
            "sucrose": {"mol_weight": 342, "mol_ratio": 4},
            "dme": {"mol_weight": 180 / 0.60, "mol_ratio": 2}
        }
        self.sugar: dict = self.sugar_types[sugar_type]


    def _str_to_float(func):
        @functools.wraps(func)
        def wrapper(*args):
            try:
                float_args = [float(arg.replace(',', '.')) if isinstance(arg, str) else arg for arg in args]
            except ValueError:
                return None
            return func(*float_args)
        return wrapper


    @_str_to_float
    def brix_to_baling(self, brix: str | int | float) -> float:
        return round(brix / 1.04, 2)


    @_str_to_float 
    def baling_to_brix(self, baling: str | int | float) -> float:
        return round(baling * 1.04, 2)


    @_str_to_float 
    def brix_to_percent(self, 
        brix_start: str | int | float, 
        brix_end: str | int | float
        ) -> float: 

        baling_start = self.brix_to_baling(brix_start)
        baling_end = self.brix_to_baling(brix_end)
        return self.baling_to_percent(baling_start, baling_end)


    @_str_to_float 
    def baling_to_percent(self, 
        baling_start: str | int | float, 
        baling_end: str | int | float
        ) -> float: 

        return round((baling_start - baling_end) / 1.938, 2)
    

    @_str_to_float 
    def how_much_sugar(self, 
        co2: str | int | float, 
        beer_liters: str | int | float, 
        temp_C: str | int | float
        ) -> float:
        
        co2_after_fermentation = 1.57 * math.pow(0.97, temp_C)
        co2_to_add = co2 - co2_after_fermentation
        co2_to_add_in_litres = co2_to_add * beer_liters
        co2_mol = co2_to_add_in_litres / 22.4

        sugar_mol = co2_mol / self.sugar['mol_ratio']
        sugar_g = sugar_mol * self.sugar['mol_weight']

        return round(sugar_g, 2)

    
    @_str_to_float 
    def sugar_solution(self, 
                    blg_start: str | int | float,
                    glucose: str | int | float
        ) -> float:

        return round(glucose * 100 / blg_start, 2)



if __name__ == "__main__":

    bc = BeerCalc()