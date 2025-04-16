import sys
import os
import runpy

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Cuando se ejecuta como un ejecutable empaquetado
        return sys._MEIPASS
    else:
        # Cuando se ejecuta desde el código fuente
        return os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta base
base_path = get_base_path()

# Agregar la ruta absoluta de 'src' al sys.path
src_path = os.path.join(base_path, "src")
sys.path.insert(0, src_path)

# Verificar si el módulo 'presentation' existe
try:
    import src.presentation
    print("Module 'presentation' imported successfully.")
except ImportError as e:
    print(f"Failed to import 'presentation': {e}")
    sys.exit(1)

if __name__ == "__main__":
    runpy.run_module("src.presentation.main", run_name="__main__")