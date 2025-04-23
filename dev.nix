nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.openssh
    pkgs.git
    pkgs.pip
    pkgs.python3Packages.pip
    pkgs.python3Packages.flask
    pkgs.python3Packages.python-dotenv
    pkgs.python3Packages.sqlalchemy
    pkgs.python3Packages.pymysql
    pkgs.python3Packages.werkzeug
  ];

  shellHook = ''
    # Create and activate venv
    if [ ! -d venv ]; then
      python3 -m venv venv
    fi
    source venv/bin/activate

    #install requirements if needed
    if [ ! -f venv/lib/python3.11/site-packages/requirements.txt ]; then
        pip install -r requirements.txt
    fi

    # Print a message to remind the user to activate the virtual environment
    echo "Virtual environment 'venv' activated. Use 'deactivate' to exit."
  '';
}