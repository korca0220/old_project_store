# -*- coding: utf-8 -*-
import sys
import os

import product_


class Common:
    """
    상품목록 공통 변수
    """
    product_common = product_.Product()
    list_product = product_common.list_product#상품목록 리스트

    def platformFunction(self):
        self.platform = sys.platform
        if(self.platform == "win32"):
            os.system('cls')
        else:
            os.system('clear')
