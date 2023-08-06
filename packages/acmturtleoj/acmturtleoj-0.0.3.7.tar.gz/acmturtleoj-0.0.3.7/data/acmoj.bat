@echo off
python3 -V > nul 2>nul && set python3="python3" || set python3="python"
pip3 -V > nul 2>nul && set pip3="pip3" || set pip3="pip"
%python3% -V | find /I "Python 3" && set pver=3 || set pver=2
%pip3% -V | find /I "python 3" && set pipv=3 || set pipv=2
if %pver% == 2 (
  echo on
  echo "You must install python3"
) else (
  if %pipv% == 2 (
	  echo on
	  echo "You must install pip3"
	) else (
	  %pip3% install --upgrade acmturtleoj -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>nul
	  echo on
	  %python3% -c "import acmturtleoj;acmturtleoj.main()"
	)
)