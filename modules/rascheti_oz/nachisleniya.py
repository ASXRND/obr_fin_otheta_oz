import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.rascheti_oz.uslugi_agentov import uslugi_agentov_itog_main
from modules.rascheti_oz.uslugi_fbo import uslugi_fbo_itog_main
from modules.rascheti_oz.drugie_uslugi import drugie_uslugi_itog_main
from modules.rascheti_oz.prod_i_reklama import prod_i_reklama_itog_main
from modules.rascheti_oz.voznagr_ozon import voznagr_ozon_itog_main
from modules.rascheti_oz.uslugi_dostavki import uslugi_dostavki_itog_main

def nachisleniya_itog_main():
    return (
        uslugi_agentov_itog_main()
        + uslugi_fbo_itog_main()
        + drugie_uslugi_itog_main()
        + prod_i_reklama_itog_main()
        + voznagr_ozon_itog_main()
        + uslugi_dostavki_itog_main()
    )


# ЗАПУСК ФУНКЦИИ
def nachisleniya_main():
    # --- УСЛУГИ АГЕНТОВ ---
    uslugi_agentov_itog = uslugi_agentov_itog_main()
    # --- УСЛУГИ FBO ---
    uslugi_fbo_itog = uslugi_fbo_itog_main()
    # --- ДРУГИЕ УСЛУГИ ---
    drugie_uslugi_itog = drugie_uslugi_itog_main()
    # --- ПРОДВИЖЕНИЕ И РЕКЛАМА ---
    prod_i_reklama_itog = prod_i_reklama_itog_main()
    # --- ВОЗНАГРАЖДЕНИЕ ОЗОН ---
    voznagr_ozon_itog = voznagr_ozon_itog_main()
    # --- УСЛУГИ ДОСТАВКИ --- 
    uslugi_dostavki_itog = uslugi_dostavki_itog_main()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (uslugi_agentov_itog + uslugi_fbo_itog + drugie_uslugi_itog + prod_i_reklama_itog + voznagr_ozon_itog + uslugi_dostavki_itog)
    print("\n================= НАЧИСЛЕНИЯ =================")
    print("Сумма:", itog, "\n")
    print("Начисления:", "Услуги агентов", uslugi_agentov_itog)
    print("Начисления:", "Услуги FBO", uslugi_fbo_itog)
    print("Начисления:", "Другие услуги", drugie_uslugi_itog)
    print("Начисления:", "Продвижение и реклама", prod_i_reklama_itog)
    print("Начисления:", "Вознаграждение ОЗОН", voznagr_ozon_itog)
    print("Начисления:",  "Услуги доставки", uslugi_dostavki_itog)
    return itog
    
    
# if __name__ == "__main__":
#  nachisleniya_main()