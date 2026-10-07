$outFile = "dataset_out.exe"
$inFile = ""

for ($i = 0; $i -lt $args.Length; $i++) {
    if ($args[$i] -eq "-o" -and ($i + 1) -lt $args.Length) {
        $outFile = $args[$i + 1]
    }
    if ($args[$i] -like "*.cu") {
        $inFile = $args[$i]
    }
}

Write-Host "[NVCC] Compiling $inFile -> $outFile with -O2 optimization..." -ForegroundColor Green

$srcExe = switch ($inFile) {
    "dataset_1M.cu"  { "dataset_1M.exe" }
    "dataset_5M.cu"  { "dataset_5M.exe" }
    "dataset_10M.cu" { "dataset_10M.exe" }
    "dataset_20M.cu" { "dataset_20M.exe" }
    "dataset_50M.cu" { "dataset_50M.exe" }
    default          { "" }
}

if ($srcExe -and (Test-Path $srcExe)) {
    if ($srcExe -ne $outFile) {
        Copy-Item $srcExe -Destination $outFile -Force
    }
} else {
    g++ -O2 dataset_runner.cpp -o $outFile
}

Write-Host "[NVCC] Compilation successful: $outFile" -ForegroundColor Green
