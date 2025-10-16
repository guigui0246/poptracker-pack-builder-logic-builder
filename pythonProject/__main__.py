import importlib
import importlib.util
import os
import sys

if sys.argv[1] == "build" or sys.argv[1] == "builder":
    old_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    spec = importlib.util.spec_from_file_location("__main__", "./builder.py", submodule_search_locations=[])
    os.chdir(old_dir)
    assert spec is not None, "builder.py not found"
    builder = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, "Failed to load builder.py"
    spec.loader.exec_module(builder)
