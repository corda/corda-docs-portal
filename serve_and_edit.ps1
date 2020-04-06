# Set $env:HUGO_PARAMS_EDITOR="atom"
# to override editor

$env:HUGO_PARAMS_SITEROOT=(Get-Location).Path.Replace("\","/")

hugo --config config.toml,config.dev.toml serve
