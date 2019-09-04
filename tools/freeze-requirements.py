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
elif 'zsh' in os.environ.get('SHELL'):
    process = Popen(
        '/bin/zsh',
        shell=False,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    print('access zsh env')
    process.stdin.write('source ./env/bin/activate\n')
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
process.stdin.flush()
process.stdin.write('git add requirements.txt\n')
process.stdin.write('deactivate')
process.stdin.flush()
process.stdin.close()
