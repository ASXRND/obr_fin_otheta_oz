from .uslugi_agentov import uslugi_agentov_main
from .uslugi_fbo import uslugi_fbo_main
from .drugie_uslugi import drugie_uslugi_main
from .prod_i_reklama import prod_i_reklama_main
from .voznagr_ozon import voznagr_ozon_main
from .uslugi_dostavki import uslugi_dostavki_main

# ЗАПУСК ФУНКЦИИ
def nachisleniya_main():
    # --- УСЛУГИ АГЕНТОВ ---
    uslugi_agentov = uslugi_agentov_main()
    # --- УСЛУГИ FBO ---
    uslugi_fbo = uslugi_fbo_main()
    # --- ДРУГИЕ УСЛУГИ ---
    drugie_uslugi = drugie_uslugi_main()
    # --- ПРОДВИЖЕНИЕ И РЕКЛАМА ---
    prod_i_reklama = prod_i_reklama_main()
    # --- ВОЗНАГРАЖДЕНИЕ ОЗОН ---
    voznagr_ozon = voznagr_ozon_main()
    # --- УСЛУГИ ДОСТАВКИ --- 
    uslugi_dostavki = uslugi_dostavki_main()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = uslugi_agentov + uslugi_fbo + drugie_uslugi + prod_i_reklama + voznagr_ozon + uslugi_dostavki
    print("\n================= НАЧИСЛЕНИЯ =================", "\n")
    print("Сумма:", itog, "\n")
    print("Начисления:","\n", " \n Услуги агентов", uslugi_agentov, "\n")
    print("Начисления", "\n",  " \n Услуги FBO", uslugi_fbo, "\n")
    print("Начисления", "\n",  " \n Другие услуги", drugie_uslugi, "\n")
    print("Начисления", "\n",  " \n Продвижение и реклама", prod_i_reklama, "\n")
    print("Начисления", "\n",  " \n Вознаграждение ОЗОН", voznagr_ozon, "\n")
    print("Начисления", "\n",  " \n Услуги доставки", voznagr_ozon, "\n")
    
# if __name__ == "__main__":
#  nachisleniya_main()