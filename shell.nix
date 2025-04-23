
{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    buildInputs = [
      pkgs.python3
      pkgs.python3Packages.flask
      pkgs.python3Packages.python-dotenv
      pkgs.python3Packages.pymysql
      pkgs.python3Packages.flask-sqlalchemy
      pkgs.python3Packages.flask-bcrypt
      pkgs.python3Packages.requests
    ];
  }