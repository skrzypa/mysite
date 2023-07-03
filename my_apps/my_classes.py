import datetime


class Calculators():

    def Bx_Blg(bx):
        blg = round(bx / 1.04, 1)
        return blg

    def Blg_Bx(blg):
        bx = round(blg * 1.04, 1)
        return bx

    def Bx_proc(bx_start, bx_end): 
        blg_start = Calculators.Bx_Blg(bx_start)
        blg_end = Calculators.Bx_Blg(bx_end)
        proc_bx = Calculators.Blg_proc(blg_start, blg_end)
        return proc_bx

    def Blg_proc(blg_start, blg_end): 
        proc_blg = round((blg_start - blg_end) / 1.938, 1)
        return proc_blg
    
    def ile_glukozy(co2, piwo, temp):
        # glukoza = (co2 * piwo) / (0.8115 + (0.0125 * temp))
        glukoza = (piwo * co2 * (temp / 20)) / (0.811 * 1000 * co2)
        glukoza = round(glukoza, 2)
        return glukoza
    
    def roztwor(bx_pocz, glukoza):
        woda_ml = round(glukoza * 100 / bx_pocz, 2)
        return woda_ml

    def style_piwne():
        grodziskie = {
                    'Styl': 'Grodziskie', 
                    'Nagazowanie minimalne.': 2.5, 
                    'Nagazowanie maksymalne': 3.1
                    }

        porter = {
                    'Styl': 'Porter', 
                    'Nagazowanie minimalne': 2.3, 
                    'Nagazowanie maksymalne': 2.9
                    }

        ipa = {
                    'Styl': 'India Pale Ale',  
                    'Nagazowanie minimalne': 2.4,  
                    'Nagazowanie maksymalne': 2.9
                    }

        stout = {
                    'Styl': 'Stout',  
                    'Nagazowanie minimalne': 2.4,  
                    'Nagazowanie maksymalne': 3.0
                    }

        witbier = {
                    'Styl': 'Witbier',  
                    'Nagazowanie minimalne': 2.6,  
                    'Nagazowanie maksymalne': 3.4
                    }

        hefeweizen = {
                    'Styl': 'Hefeweizen',  
                    'Nagazowanie minimalne': 2.2,  
                    'Nagazowanie maksymalne': 2.8
                    }

        style_piwne = [grodziskie, porter, ipa, stout, witbier, hefeweizen]
        
        return style_piwne

        # for piwo in style_piwne:                            # iteracja przez listę
        #     for key, value in piwo.items():                 # iteracja przez k i v słownika 
        #         print(f"{key} \033[96m{value}\033[0m")      # wyświetlenie k i v słownika


class GenerateCalendar():
    months_dict = {'Styczeń': '01', 'Luty': '02', 'Marzec': '03', 'Kwiecień': '04', 
               'Maj': '05', 'Czerwiec': '06', 'Lipiec': '07', 'Sierpień': '08', 
               'Wrzesień': '09', 'Październik': '10', 'Listopad': '11', 'Grudzień': '12'} 

    month_list_1 = list(months_dict.keys())     # ['Styczeń', 'Luty', ...]
    month_list_2 = list(months_dict.values())   # ['01', '02', ...]

    day_today = datetime.date.today().strftime('%d')
    # month_today = datetime.date.today().strftime('%m')
    month_today = month_list_1[int(datetime.date.today().strftime('%m')) -1]      # xD zadziałało np. Luty
    month_today_2 = month_list_2[int(datetime.date.today().strftime('%m')) -1]     # np. '02'
    year_today = datetime.date.today().strftime('%Y')
    
    years_list = [str(x) for x in range(2022, int(year_today)+2)]
    years_list = years_list[::-1]