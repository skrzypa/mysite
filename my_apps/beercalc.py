from .models import BeerStyles


class BeerCalc():

    def Bx_Blg(bx):
        blg = round(bx / 1.04, 1)
        return blg

    def Blg_Bx(blg):
        bx = round(blg * 1.04, 1)
        return bx

    def Bx_proc(bx_start, bx_end): 
        blg_start = BeerCalc.Bx_Blg(bx_start)
        blg_end = BeerCalc.Bx_Blg(bx_end)
        proc_bx = BeerCalc.Blg_proc(blg_start, blg_end)
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
        return BeerStyles.objects.all()