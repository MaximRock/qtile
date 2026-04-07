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
}
