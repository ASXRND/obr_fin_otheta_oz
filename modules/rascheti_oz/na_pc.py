import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.rascheti_oz.proda_i_vozvrati import proda_i_vozvrati_itog_main 
from modules.rascheti_oz.nachisleniya import nachisleniya_itog_main
from modules.rascheti_oz.prochie_nachisleniya import prochie_nachisleniya_itog_main

def na_pc_itog_main():
    return (
        proda_i_vozvrati_itog_main()
        + nachisleniya_itog_main()
        + prochie_nachisleniya_itog_main()
    )

# ЗАПУСК ФУНКЦИИ
def na_pc_main():
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (na_pc_itog_main())
    print("\n================= НА РС =================")
    print("Сумма:", itog, "\n")
    

# if __name__ == "__main__":
# 		na_pc_main() 
    