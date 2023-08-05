#When Python2 support is droped, remove this pkgutil-style file for native python3 namespaces
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
