"""
__main__.py module entry point
"""
import sys
from nixconverter import eegbase_nix_converter


if __name__ == "__main__":
    eegbase_nix_converter.main(sys.argv[1:])
