import requests
import datetime
import json



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



class CurrencyExchangeRatesSince2002():
    def __init__(self):
        self.link = "https://api.nbp.pl/api/exchangerates/tables/A/"
        self.start_date = datetime.date(2002, 1, 1)
        self.end_date = datetime.date.today()
        self.days = (self.end_date - self.start_date).days

        self.range_dates = list(range(0, self.days + 1, 94)) # limit of up to 93 days
        if self.days + 1 not in self.range_dates:
            self.range_dates.append(self.days + 1)
    

    def links_list(self) -> list[str]:
        """ All links with rates from 2002-01-01 to today """
        links = []
        for i, j in zip(self.range_dates[:-1], self.range_dates[1:]):
            links.append(
                self.link + f"{self.start_date + datetime.timedelta(days= i)}/{self.start_date + datetime.timedelta(days= j-1)}"
            )
        return links
    

    def records(self, link: str) -> list[dict] | None:
        """ Records in one link """
        get = requests.get(url= link)
        if get.status_code == 200:
            get = get.json()
            return get
        return None 
            



if __name__ == "__main__":
    from pprint import pprint
    
    # CC = CurrencyCalc()
    # pprint(CC.currencies)

    cc: CurrencyExchangeRatesSince2002 = CurrencyExchangeRatesSince2002()
    for nr, link in enumerate(cc.links_list(), start= 1):
        print(nr, link, sep=". ")
        # records = cc.records(link)
        # if records != None:
            # for record in records:
            #     print(record) # save in db
            #     print('**************************')
            # break