import importlib
import os
import traceback
from typing import Dict, Any

_cache: Dict[str, Dict[str, Any]] = {}  # Cache for loaded modules

def dynamic_load_submodules(package_name: str, package_path: str) -> None:
    """
    Dynamically loads all submodules of a given package.

    Args:
        package_name (str): Full package name (e.g., `files.formats`).
        package_path (str): Absolute path to the package directory.

    Returns:
        Dict[str, Any]: A dictionary mapping submodule names to their imported modules.
    """
    # Dynamically load all submodules into the package namespace
    if package_name not in _cache:
        modules = {}
        package_path = os.path.dirname(os.path.abspath(package_path))
        for file in os.listdir(package_path):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"{package_name}.{module_name}")
                    modules[module_name] = module
                except Exception as e:
                    tb = traceback.format_exc()
                    raise ImportError(
                        f"Failed to import module '{module_name}' in '{package_name} ({package_path})': {e}\n\nOriginal traceback:\n{tb}"
                ) from e

    globals().update(_cache[package_name])

    # Define `__getattr__` for lazy loading
    def __getattr__(name):
        try:
            module = importlib.import_module(f"{package_name}.{name}")
            return module
        except ModuleNotFoundError:
            raise AttributeError(f"Module '{name}' not found in package '{package_name}'")

    globals()["__getattr__"] = __getattr__
