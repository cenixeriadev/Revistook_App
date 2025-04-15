import sys
import os
import runpy

if getattr(sys, 'frozen', False):
    
    base_path = sys._MEIPASS
else:
    
    base_path = os.path.dirname(os.path.abspath(__file__))


sys.path.insert(0, os.path.join(base_path, "src"))

if __name__ == "__main__":
    runpy.run_module("presentation.main", run_name="__main__")
