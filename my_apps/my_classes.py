


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

        return [grodziskie, porter, ipa, stout, witbier, hefeweizen]

        # for piwo in style_piwne:                            # iteracja przez listę
        #     for key, value in piwo.items():                 # iteracja przez k i v słownika 
        #         print(f"{key} \033[96m{value}\033[0m")      # wyświetlenie k i v słownika
