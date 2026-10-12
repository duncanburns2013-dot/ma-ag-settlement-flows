# Local OCR with the built-in Windows engine. Usage: ocr_run.ps1 <png folder> <output folder> [file pattern]
param([string]$InDir, [string]$OutDir, [string]$Pattern = "*.png")
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, $type) {
    $t = $asTask.MakeGenericMethod($type).Invoke($null, @($op))
    $null = $t.Wait(-1)
    $t.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$files = Get-ChildItem -Path $InDir -Filter $Pattern | Sort-Object Name
$n = 0
foreach ($f in $files) {
    $dest = Join-Path $OutDir ($f.BaseName + ".txt")
    if (Test-Path $dest) { continue }
    $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
    $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
    [System.IO.File]::WriteAllText($dest, $res.Text, (New-Object System.Text.UTF8Encoding($false)))
    $stream.Dispose()
    $n++
    if ($n % 50 -eq 0) { Write-Output "ocr $n / $($files.Count)" }
}
Write-Output "done: $n pages OCR'd"
