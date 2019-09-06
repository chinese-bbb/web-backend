import os
from subprocess import PIPE
from subprocess import Popen

if os.name == 'nt':
    process = Popen(
        'powershell.exe',
        shell=False,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    process.stdin.write('./env/Scripts/activate\n')
    process.stdin.write('$PSDefaultParameterValues["Out-File:Encoding"] = "ASCII"\n')
else:
    process = Popen(
        '/bin/sh',
        shell=False,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    process.stdin.write('source ./env/bin/activate\n')

process.stdin.write('pip freeze > requirements.txt\n')
process.stdin.write('git add requirements.txt\n')
process.stdin.write('deactivate')
process.stdin.close()
process.stdout.read()
