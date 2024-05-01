import datetime
import calendar
import pprint



class Meetings():
    def __init__(self):
        self.date_format =                          "%Y-%m-%d %H:%M:%S"
        self.date_today: datetime.datetime =        datetime.datetime.now()
        self.formatted_date_today: str =            self.date_today.strftime(self.date_format)
        self.year_progress: float =                 self._year_progress()
        self.year_range: list =                     list(range(2023, self.date_today.year + 2))
        self.year_today: int =                      self.date_today.year
        self.days: list[str] =                      ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb', 'Nd']
        self.months: list[str] =                    ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
        self.hours: list[str] =                     [str(h).zfill(2) for h in range(0, 24)]
        self.minutes: list[str] =                   [str(m).zfill(2) for m in range(0, 60)]
        
    
    def generate_calendar(self, year: int = None) -> dict:
        if year is None:
            year = self.year_today

        calendar_ = calendar.Calendar().yeardayscalendar(year, width= 1)
        formatted_calendar = {month: [] for month in self.months}

        for mnr, month in enumerate(calendar_):
            for wnr, week in enumerate(month[0]):
                w = []
                for dnr, day in enumerate(week):
                    w.append(str(calendar_[mnr][0][wnr][dnr]).zfill(2))
                formatted_calendar[list(formatted_calendar.keys())[mnr]].append(w)

        return formatted_calendar
        

    def _year_progress(self) -> float:
        year_today = self.date_today.year
        past_days = int(self.date_today.strftime("%j"))
        year_progress = (past_days * 100) / (365 + calendar.isleap(year_today))
        return round(year_progress, 1)


    


if __name__ == "__main__":
    obj: Meetings = Meetings()
    for k, v in obj.__dict__.items():
        print(f"{k}: {v}")

    print(obj.generate_calendar(2024), type(obj.generate_calendar(2024)))