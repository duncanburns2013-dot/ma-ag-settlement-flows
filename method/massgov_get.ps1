# Fetch one mass.gov page or document with the browser headers the site's filter expects (it rejects bare requests).
# Usage: powershell -File massgov_get.ps1 -Url <url> -Out <file> [-Referer <page the link came from>]
param([string]$Url, [string]$Out, [string]$Referer = "https://www.mass.gov/")
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
curl.exe -sS -L --compressed --ssl-no-revoke -m 60 -o $Out `
  -H "User-Agent: $ua" `
  -H "Accept: text/html,application/xhtml+xml,*/*;q=0.8" `
  -H "Accept-Language: en-US,en;q=0.9" `
  -H "Referer: $Referer" `
  -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" `
  -w "%{http_code} %{size_download}`n" $Url
