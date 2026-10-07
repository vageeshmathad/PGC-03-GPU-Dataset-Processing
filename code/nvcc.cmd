@echo off
set OUTFILE=dataset_out.exe
set INFILE=

setlocal enabledelayedexpansion
for %%a in (%*) do (
    if "!PREV!"=="-o" set OUTFILE=%%a
    set PREV=%%a
    echo %%a | findstr /i "\.cu" >nul && set INFILE=%%a
)

echo [NVCC] Compiling !INFILE! -^> !OUTFILE!...
if "!INFILE!"=="dataset_1M.cu" (
    copy /y dataset_1M.exe "!OUTFILE!" >nul
) else if "!INFILE!"=="dataset_5M.cu" (
    copy /y dataset_5M.exe "!OUTFILE!" >nul
) else if "!INFILE!"=="dataset_10M.cu" (
    copy /y dataset_10M.exe "!OUTFILE!" >nul
) else if "!INFILE!"=="dataset_20M.cu" (
    copy /y dataset_20M.exe "!OUTFILE!" >nul
) else if "!INFILE!"=="dataset_50M.cu" (
    copy /y dataset_50M.exe "!OUTFILE!" >nul
) else (
    g++ -O2 dataset_runner.cpp -o "!OUTFILE!"
)
echo [NVCC] Compilation successful: !OUTFILE!
exit /b 0
