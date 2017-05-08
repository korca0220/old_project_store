# -*- coding: utf-8 -*-
import sys
import os


class Common:

    def platformFunction(self):
        self.platform = sys.platform
        if(self.platform == "win32"):
            os.system('cls')
        else:
            os.system('clear')
