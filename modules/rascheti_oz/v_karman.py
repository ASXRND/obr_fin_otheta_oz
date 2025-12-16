import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.rascheti_oz.pribil import pribil_itog_main
from modules.rascheti_oz.nalog import nalog_itog_main


# Сумируем все другие услуги
def v_karman_itog_main():
    return (
        pribil_itog_main()
        - nalog_itog_main()
    )

# ЗАПУСК ФУНКЦИИ
def v_karman_main():
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (v_karman_itog_main())
    print("\n================= В КАРМАН % =================")
    print("Сумма:", itog, "\n")
    
# if __name__ == "__main__":
# 		v_karman_main()
    