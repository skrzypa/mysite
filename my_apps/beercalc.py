"""
Sources:
    https://github.com/Brewtarget/brewtarget/blob/develop/src/PrimingDialog.cpp
    https://piwko.com.pl/ 
    https://twojbrowar.pl/pl/blog/jak-zmierzyc-poziom-alkoholu-w-domowym-piwie 
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


    # def _str_to_float(self, value: str) -> float | None:
        # value = value.replace(',', '.')

        # try:
        #     value = float(value)
        # except ValueError or TypeError:
        #     return None
        
        # return value


    def _str_to_float(func):

        @functools.wraps(func)
        def wrapper(*args):

            try:
                float_args = [float(arg) if isinstance(arg, str) else arg for arg in args]
            except ValueError:
                return None
            
            return func(*float_args)
        
        return wrapper


    @_str_to_float
    def brix_to_baling(self, brix: str) -> float:
        # brix: float = self._str_to_float(brix)

        # if brix is None:
        #     return None
        
        return round(brix / 1.04, 2)


    @_str_to_float 
    def baling_to_brix(self, baling: str) -> float:
        # baling: float = self._str_to_float(baling)

        # if baling is None:
        #     return None
        
        return round(baling * 1.04, 2)


    @_str_to_float 
    def brix_to_percent(self, brix_start: str, brix_end: str) -> float: 

        baling_start = str(self.brix_to_baling(brix_start))
        baling_end = str(self.brix_to_baling(brix_end))

        # if baling_start is None or baling_end is None:
        #     return None

        return self.baling_to_percent(baling_start, baling_end)


    @_str_to_float 
    def baling_to_percent(self, baling_start: str, baling_end: str) -> float: 
        #baling_start: float = self._str_to_float(baling_start)
        # baling_end: float = self._str_to_float(baling_end)

        # if baling_start is None or baling_end is None:
        #     return None

        return round((baling_start - baling_end) / 1.938, 2)
    

    @_str_to_float 
    def how_much_sugar(self, co2: str, beer_liters: str, temp_C: str) -> float:
        # co2 = self._str_to_float(co2)
        # beer_liters = self._str_to_float(beer_liters)
        # temp_C = self._str_to_float(temp_C)

        # if co2 is None or beer_liters is None or temp_C is None:
        #     return None

        co2_after_fermentation = 1.57 * math.pow(0.97, temp_C)
        co2_to_add = co2 - co2_after_fermentation
        co2_to_add_in_litres = co2_to_add * beer_liters
        co2_mol = co2_to_add_in_litres / 22.4

        sugar_mol = co2_mol / self.sugar['mol_ratio']
        sugar_g = sugar_mol * self.sugar['mol_weight']

        return round(sugar_g, 2)

    
    @_str_to_float 
    def sugar_solution(self, brix_start: str, glucose: str) -> float:
        # brix_start = self._str_to_float(brix_start)
        # glucose = self._str_to_float(glucose)

        # if brix_start is None or glucose is None:
        #     return None

        return round(glucose * 100 / brix_start, 2)



if __name__ == "__main__":

    bc = BeerCalc()
    print(
        bc.brix_to_baling("21") == 20.19,
        bc.baling_to_brix("14") == 14.56,
        bc.baling_to_percent('15', '3') == 6.19,
        bc.brix_to_percent('18', '4') == 6.95,
        bc.how_much_sugar('2.5', '20', '22') == 136.34,
        bc.sugar_solution('18', '136.34') == 757.44,
        
        bc.brix_to_baling("21a"),
        bc.baling_to_brix("14a"),
        bc.brix_to_percent('18a', '4'),
        bc.baling_to_percent('15', '3a'),
        bc.how_much_sugar('2.5', '20a', '22'),
        bc.sugar_solution('18', '136.34a'),
        sep='\n'
    )