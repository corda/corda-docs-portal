$env:HUGO_PARAMS_SITEROOT=(Get-Location).Path.Replace("\","/")
hugo --config config.toml,config.dev.toml serve
