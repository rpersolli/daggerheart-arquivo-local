@echo off
cd /d "%~dp0"
echo Acesso para aparelhos na mesma rede Wi-Fi. Sem contas ou senhas.
echo Use o IPv4 deste computador e a porta 8765 no navegador do celular.
ipconfig
python server.py --lan
pause
