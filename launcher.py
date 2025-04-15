import runpy
import sys
import os
import runpy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

if __name__ == "__main__":
    runpy.run_module("presentation.main", run_name="__main__")
