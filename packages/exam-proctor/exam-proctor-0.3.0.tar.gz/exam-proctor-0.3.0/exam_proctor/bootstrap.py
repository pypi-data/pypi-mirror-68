import sys

def main():
    if "check" in sys.argv:
        from . import permissions
        permissions.check_permissions()
    else:
        from . import web
        web.main_tray()

