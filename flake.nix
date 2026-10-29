{
  description = "Packaging QLog in Nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        pypkgs = pkgs.python3Packages;

        qlog = pypkgs.buildPythonPackage {
          pname = "qlog";
          version = "2026.4.28";
          src = ./.;

          pyproject = true;
          build-system = [ pypkgs.setuptools ];

          dependencies = [
            pypkgs.requests
            pypkgs.pyyaml
            pypkgs.lxml
            pypkgs.cssselect
            pypkgs.colorama
          ];
        };
      in
      {
        packages.default = qlog;
      }
    );
}
