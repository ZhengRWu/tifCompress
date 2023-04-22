@echo off
setlocal enabledelayedexpansion

for %%i in (*) do (
  set "filename=%%~ni"
  set "extension=%%~xi"
  set "newfilename=!filename:ZIP.=!"
  if not "!newfilename!" == "!filename!" (
    ren "%%i" "!newfilename!!extension!"
  )
)

echo All done!
pause
