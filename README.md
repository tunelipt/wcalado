# wmesa

Um programa para controlar a mesa giratória do túnel de vento




## Como criar os executáveis em windows

 * `mesaxmlrpc.exe`: `pyinstaller --onefile --icon wmesalib\ipt-wmesa.ico mesaxmlrpc.py`
 * `wmesacliente.exe`: `pyinstaller --onefile --icon wmesalib\ipt-wmesa.ico --noconsole wmesacliente.py`
 * `wmesa.exe`: `pyinstaller --onefile --icon ipt-wmesalib\wmesa.ico wmesa.py`