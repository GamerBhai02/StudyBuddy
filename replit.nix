{ pkgs }: {
  deps = [
    pkgs.nodejs_20
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.postgresql
    pkgs.nodePackages.npm
    pkgs.nodePackages.typescript
    pkgs.bash
  ];
}
