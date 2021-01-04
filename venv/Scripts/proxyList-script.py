#!c:\users\leo\desktop\cargofax\05_shipping_scrape\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'http-request-randomizer==1.3.1','console_scripts','proxyList'
__requires__ = 'http-request-randomizer==1.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('http-request-randomizer==1.3.1', 'console_scripts', 'proxyList')()
    )
