---
date: '2023-09-01'
title: "Export Interoperability Identity Endpoint"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-export-identity
    parent: corda5-interop-admin
    weight: 4000
section_menu: corda5
---

# Export Interoperability Identity Endpoint

You can use the `exportInterOpIdentity` endpoint to export an Interoperability identity and group policy information as
a JSON string so that it can be added to the systems of other Interoperability peers.

The endpoint is invoked by calling the `GET` method on `/interop/{holdingIdentityShortHash}/export/identity/{interopIdentityShortHash}` where:

* The `holdingIdentityShortHashis` the short hash of the holding identity to export Interoperability identity from
* The `interopIdentityShortHash` is the short hash of the Interoperability identity to export

It returns an `ExportInteropIdentityRest.Response` object.

Response message example:

```json
{
  "members": [
    {
      "x500Name": "O=Gold, L=London, C=GB",
      "owningIdentityShortHash": "1750C7ECD7B4",
      "endpointUrl": "<https://corda-p2p-gateway-worker.corda:8080>",
      "endpointProtocol": "1",
      "facadeIds": [
        "org.corda.interop/platform/tokens/v1.0",
        "org.corda.interop/platform/tokens/v2.0"
      ]
    }
  ],
  "groupPolicy": {
    "fileFormatVersion": 1,
    "groupId": "13fae7c9-a234-4a7a-8613-375d663b158f",
    "p2pParameters": {
      "sessionTrustRoots": [],
      "tlsTrustRoots": [
        "-----BEGIN CERTIFICATE-----\\nMIIFHjCCBAagAwIBAgISAy1ybKW9u73QQxLAktLHTEQQMA0GCSqGSIb3DQEBCwUA\\nMDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQD\\nEwJSMzAeFw0yMjA1MTExNTAxMDZaFw0yMjA4MDkxNTAxMDVaMBExDzANBgNVBAMT\\nBnIzLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMqmvfMOna/+\\nr0V3d3hpGPz5hesAAJRZjJCjsQr5ly8LodIfcPRSz+p5N8ui6ct8lyOmGLmiVzKn\\n6h+On4ilNnd2inIqBRcyFlU4YFyBqq9+FZdR64gEr2CVX8xDz5bMFymLZJoCDnKg\\nzq6LAvhQv/2NIkSRuLI09phKhMwQkAzFaOx0Q1kkmNnJYSf81dF1lbTVAAEHsxMK\\n+4dGECQCYFsfkrpk4wVBnaIdr7JLsrOHbbdLK8Ks/TxVNw20FOvuKZzR28lFZ2ro\\nWY7S3s+x6mNZk4zhmTkBFXR747q7IVqj+Un3BU2G5/2TZ6LCJ+8m3WPD+9gzMHdf\\nNwDftNqTuMkCAwEAAaOCAk0wggJJMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAU\\nBggrBgEFBQcDAQYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUtd2w\\n7gkV6EYKUVTrXLPbKNpIc1UwHwYDVR0jBBgwFoAUFC6zF7dYVsuuUAlA5h+vnYsU\\nwsYwVQYIKwYBBQUHAQEESTBHMCEGCCsGAQUFBzABhhVodHRwOi8vcjMuby5sZW5j\\nci5vcmcwIgYIKwYBBQUHMAKGFmh0dHA6Ly9yMy5pLmxlbmNyLm9yZy8wHQYDVR0R\\nBBYwFIIGcjMuY29tggp3d3cucjMuY29tMEwGA1UdIARFMEMwCAYGZ4EMAQIBMDcG\\nCysGAQQBgt8TAQEBMCgwJgYIKwYBBQUHAgEWGmh0dHA6Ly9jcHMubGV0c2VuY3J5\\ncHQub3JnMIIBBAYKKwYBBAHWeQIEAgSB9QSB8gDwAHYAKXm+8J45OSHwVnOfY6V3\\n5b5XfZxgCvj5TV0mXCVdx4QAAAGAs9o+JQAABAMARzBFAiEAi07Xbw6nqHBtGQzN\\nLXbCPx68E2xYa9M/ytztzJb96IYCIAiIc9y7u2H510F8AQ1zon7wDQjaTTvL3Ezl\\nJBgFK02aAHYAQcjKsd8iRkoQxqE6CUKHXk4xixsD6+tLx2jwkGKWBvYAAAGAs9o+\\nZwAABAMARzBFAiEAyO7PeW40ocwt+QqSMZAJHKRe7Ip1kYkjUhabhVQD0CoCIBpD\\nqJEJd3UlGIUyxJ44i72xQ6kvn5adfnmJE5Jh8YwPMA0GCSqGSIb3DQEBCwUAA4IB\\nAQBRENd2mg7C73zwxAduIDcYaQ+bKaM9+edHBC+h7cDSACdQ1J+AKruWWYOfQJXG\\nQvudeDU2W7+kUC/0fq0Ui9cGCQBY+EacFN6261z2jVLtdGwJWRe2pYwIVOdknFet\\nMY31Fqih/HToiaX1Fz0qkN0TrdLBsMIZEx3XAiMHbJH4AOrr+V2FpV6GIAZ1A68I\\nFkR4W6zPnI7cwjpeLnO6x1A92y5txtNBeBu0DDnbt695J8BVZeJBei0gIVe3y1Xf\\n2xPJfCYMCpysD6ADGOmMrahZ4ANfDck27hIDw8GXYDBp8XP7teM7r/OVRJW5MJUK\\nxcTyC7ANrJ7GGChxJZUaq0Qu\\n-----END CERTIFICATE-----\\n"
      ],
      "sessionPki": "Standard",
      "tlsPki": "Standard",
      "tlsVersion": "1.3",
      "protocolMode": "Authenticated_Encryption",
      "tlsType": "OneWay"
    }
  }
}

```
