import requests



class CurrencyCalc():
    def __init__(self):
        self.link = "http://api.nbp.pl/api/exchangerates/tables/a/"
    

    @property
    def currencies(self) -> dict:
        return requests.get(url= self.link).json()[0]
    

    def pln_to_other(self, amount: str, mid: float) -> float | None:
        amount = self._str_to_float(amount)
        if amount is None:
            return None
        return round(amount / mid, 4)


    def other_to_pln(self, amount: str, mid: float) -> float | None:
        amount = self._str_to_float(amount)
        if amount is None:
            return None
        return round(amount * mid, 4)
    

    def _str_to_float(self, amount: str) -> float | None:
        try:
            amount = float(amount)
        except ValueError:
            return None
        return float(amount)



if __name__ == "__main__":
    from pprint import pprint
    
    CC = CurrencyCalc()
    pprint(CC.currencies)