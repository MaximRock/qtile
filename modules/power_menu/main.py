#!/usr/bin/env nix-shell
#! nix-shell -i python3 ../../shell.nix

from modules.power_menu.app import Application


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
