# -*- coding: utf-8 -*-
import sys
import os

import product_



class Common:

    product_common = product_.Product()
    """
    상품목록 공통 변수
    """
    list_product = product_common.list_product#상품목록 리스트

    """
    상품판매 공통변수
    """



    def platformFunction(self):
        self.platform = sys.platform
        if(self.platform == "win32"):
            os.system('cls')
        else:
            os.system('clear')
