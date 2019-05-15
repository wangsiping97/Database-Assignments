from src.shell import *


shell = Shell()
try: 
    shell.run()
except: 
    print("\n可能是由于窗口未正常关闭发生的错误。\n")