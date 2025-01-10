from app.kernel.utils.dynamic_loader import dynamic_load_submodules; globals().update(dynamic_load_submodules(__name__, __file__))
