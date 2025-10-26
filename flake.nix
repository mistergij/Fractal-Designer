{
  description = "virtual environments";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    devshell.url = "github:numtide/devshell";
    flake-utils.url = "github:numtide/flake-utils";
  

    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };

    nixpkgs-python.inputs.nixpkgs.follows = "nixpkgs";
    devshell.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    {
      self,
      flake-utils,
      devshell,
      nixpkgs,
      nixpkgs-python,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShells.default =
        let
          pkgs = import nixpkgs {
            inherit system;

            overlays = [ devshell.overlays.default ];
          };

          pythonVersion = "3.13";

          lib = nixpkgs.lib;

          python = nixpkgs-python.packages.${system}.${pythonVersion};
          pythonldlibpath = lib.makeLibraryPath (with pkgs; [
            zlib zstd stdenv.cc.cc curl openssl attr libssh bzip2 libxml2 acl libsodium util-linux xz systemd kdePackages.qtwayland stdenv.cc.cc.lib libGL libxkbcommon fontconfig xorg.libX11 glib freetype dbus kdePackages.wayland
          ]);

          env = (python.withPackages (python-pkgs: with python-pkgs; [
            pytest
            setuptools
            wheel
            venvShellHook
          ])).overrideAttrs {
              allowSubstitutes = false;
          };
          wrapPrefix = if (!pkgs.stdenv.isDarwin) then "LD_LIBRARY_PATH" else "DYLD_LIBRARY_PATH";
          patchedpython = (pkgs.symlinkJoin {
            name = "python";
            paths = [ env ];
            buildInputs = [ pkgs.makeWrapper ];
            postBuild = ''
              wrapProgram "$out/bin/python${pythonVersion}" --prefix ${wrapPrefix} : "${pythonldlibpath}"
            '';
          });
        in
          pkgs.mkShell {
            name = "lab-5";
            packages = with pkgs; [
              patchedpython
              gcc
              kdePackages.qtwayland
              libffi
              openssl
              ruff
              unzip
              uv
            ];
            venvDir = ".venv";
            buildInputs = [
              python.pkgs.venvShellHook
              python.pkgs.virtualenv
              python.pkgs.pip
              python.pkgs.setuptools
              pkgs.kdePackages.qtwayland
            ];
            src = null;
            shellHook = ''
              export PS1='\n\[\e[1;32m\][\[\e]0;\u@\h: \w\a\]\u@\h:\w]\[\e[91;1m\]$(__git_ps1 " (%s)")\[\e[0;35m\] (lab-5) \[\e[97;1m\]\$\[\e[0m\] '
              virtualenv --no-setuptools $venvDir
            '';
            postShellHook = ''
              ln -sf PYTHONPATH/* $venvDir/lib/python${pythonVersion}/site-packages
            '';
            PATH="$PWD/bin:$PATH";
            PYTHONPATH="$PWD/$venvDir/${python.sitePackages}:$PYTHONPATH";
            QT_PLUGIN_PATH="${pkgs.kdePackages.qtwayland}/lib/qt-6/plugins}";
            QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.kdePackages.qtwayland}/lib/qt-6/plugins/platforms";
            LD_LIBRARY_PATH = "${pythonldlibpath}";
          };
    });
}
