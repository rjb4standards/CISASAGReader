REM Requires variable expansion to be enabled cmd /V
@echo off
setlocal

set "ResultFile=SAGresults.txt"
set "folder_path=C:\users\dick\SAGSPDfiles"
for %%f in (%folder_path%\*) do ( 
echo "PROCESSING FILE: " %%f
pause  
call sag-reader --include-descriptions %%f 
set /P "PassFail=Pass or Fail?"
echo %%f,!PassFail!, %DATE%, %TIME% >> %ResultFile%)
echo Results are stored in: %ResultFile%
