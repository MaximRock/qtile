{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python313.withPackages (
      p: with p; [
        customtkinter
        tkinter
        pillow
      ]
    ))
    tk
    jetbrains-mono
    fira-code
    fontconfig
    ruff
  ];

  shellHook = ''
    export PYTHONPATH="$HOME/.config/qtile:$PYTHONPATH"
    if [ -d "$HOME/.fonts" ]; then
      chmod -R u+rw "$HOME/.fonts" 2>/dev/null || true
    fi
    echo "✓ Qtile dev environment loaded" 
    echo "✓ Ruff available: $(ruff --version)"

  '';

  # shellHook = ''
  #   # 1. Добавляем конфиг Qtile в PYTHONPATH
  #   export PYTHONPATH="$HOME/.config/qtile:$PYTHONPATH"

  #   # 2. Настраиваем шрифты декларативно
  #   # Создаем локальную директорию для кэша шрифтов (не требует sudo)
  #   export FONTCONFIG_CACHE_DIR="$HOME/.cache/fontconfig"
  #   mkdir -p "$FONTCONFIG_CACHE_DIR"

  #   # Указываем путь к шрифтам из Nix store
  #   export FONTCONFIG_PATH="${pkgs.jetbrains-mono}/share/fonts/truetype:${pkgs.fontconfig.out}/etc/fonts"

  #   # Обновляем кэш шрифтов для текущей сессии
  #   fc-cache -f "$FONTCONFIG_PATH" > /dev/null 2>&1 || true
  #       # 3. Исправляем права на ~/.fonts если папка существует (чтобы убрать ошибку)
  #   if [ -d "$HOME/.fonts" ]; then
  #     chmod -R u+rw "$HOME/.fonts" 2>/dev/null || true
  #   fi

  #   echo "✓ Shell ready with JetBrains Mono and customtkinter"
  # '';
}
