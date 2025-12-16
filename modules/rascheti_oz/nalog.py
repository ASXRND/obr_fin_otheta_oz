import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.rascheti_oz.na_pc import na_pc_itog_main


def nalog_itog_main():
    return (
        na_pc_itog_main()
        * 0.07
    )

# ЗАПУСК ФУНКЦИИ
def nalog_main():
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (nalog_itog_main())
    print("\n================= НАЛОГ 7 % =================")
    print("Сумма:", itog, "\n")
    return itog
    
    
if __name__ == "__main__":
		nalog_itog_main()		