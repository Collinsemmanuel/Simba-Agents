import sys
import os
from dreamforge.cli import run_cli

if __name__ == "__main__":
    # Ensure the script can find the dreamforge module
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'dreamforge')))
    run_cli()