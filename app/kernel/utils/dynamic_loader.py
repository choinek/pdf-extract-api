import importlib
import os
from typing import Dict, Any

_cache: Dict[str, Dict[str, Any]] = {}  # Cache for loaded modules


def dynamic_load_submodules(package_name: str, package_path: str) -> Dict[str, Any]:
    """
    Dynamically loads all submodules of a given package.

    Args:
        package_name (str): Full package name (e.g., `files.formats`).
        package_path (str): Absolute path to the package directory.

    Returns:
        Dict[str, Any]: A dictionary mapping submodule names to their imported modules.
    """
    if package_name in _cache:
        return _cache[package_name]  # Return cached modules if already loaded

    package_path = os.path.dirname(os.path.abspath(package_path))

    print (f"Loading submodules from {package_name}...")
    print (f"Package path: {package_path}")
    modules = {}
    for file in os.listdir(package_path):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]  # Strip ".py" from the filename
            try:
                module = importlib.import_module(f"{package_name}.{module_name}")
                modules[module_name] = module
            except Exception as e:
                print (f"Error importing module '{module_name}' in '{package_name}': {e}")
                raise ImportError(f"Failed to import module '{module_name}' in '{package_name}': {e}")

    _cache[package_name] = modules  # Cache the loaded modules
    return modules
