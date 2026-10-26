param([string]$Source,[string]$Destination)
Add-Type -AssemblyName System.Drawing
if (Test-Path -LiteralPath $Destination) { throw "Output already exists: $Destination" }
$parent = Split-Path -Parent $Destination
New-Item -ItemType Directory -Path $parent -Force | Out-Null
$im = [System.Drawing.Image]::FromFile($Source)
try {
  $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $parameters = New-Object System.Drawing.Imaging.EncoderParameters 1
  try {
    $parameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality),([long]92)
    $im.Save($Destination,$codec,$parameters)
  } finally { $parameters.Dispose() }
} finally { $im.Dispose() }
$check = [System.Drawing.Image]::FromFile($Destination)
try {
  if ($check.Width -ne $check.Height) { throw 'Output is not square' }
  if ((Get-Item -LiteralPath $Destination).Length -ge 1000000) { throw 'Output exceeds 1 MB' }
  Write-Output "$($check.Width)x$($check.Height) $((Get-Item -LiteralPath $Destination).Length) bytes"
} finally { $check.Dispose() }
