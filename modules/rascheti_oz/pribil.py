
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.rascheti_oz.na_pc import na_pc_itog_main
from modules.rascheti_oz.kol_vo_prod_ed import kol_vo_prod_ed_itog_main


def pribil_itog_main():
    return (
        na_pc_itog_main()
        - kol_vo_prod_ed_itog_main()
    )

# ЗАПУСК ФУНКЦИИ
def pribil_main():
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (pribil_itog_main())
    print("\n================= ПРИБЫЛЬ ==================")
    print("Сумма:", itog, "\n")
    return itog
    
# if __name__ == "__main__":
# 		pribil_main()		
    