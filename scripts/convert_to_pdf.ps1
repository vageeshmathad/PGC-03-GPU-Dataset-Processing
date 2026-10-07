$pptxPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\presentation\CUDA_GPU_Dataset_Processing_Enhanced.pptx'
$pdfPptxPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\presentation\CUDA_GPU_Dataset_Processing_Enhanced.pdf'

Write-Host "Opening PowerPoint..."
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$pres.SaveAs($pdfPptxPath, 32)
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "Converted PPTX to PDF successfully: $pdfPptxPath"

$docxPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\report\Experiment_3_GPU_Dataset_Processing_Report.docx'
$pdfDocxPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\report\Experiment_3_GPU_Dataset_Processing_Report.pdf'

$guideDocxPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\How_To_Run_Commands_Guide.docx'
$guidePdfPath = 'c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\How_To_Run_Commands_Guide.pdf'

Write-Host "Opening Word..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

$doc1 = $word.Documents.Open($docxPath)
$doc1.SaveAs([ref]$pdfDocxPath, [ref]17)
$doc1.Close()

$doc2 = $word.Documents.Open($guideDocxPath)
$doc2.SaveAs([ref]$guidePdfPath, [ref]17)
$doc2.Close()

$word.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Host "Converted DOCX to PDF successfully: $pdfDocxPath"
Write-Host "Converted Guide to PDF successfully: $guidePdfPath"
