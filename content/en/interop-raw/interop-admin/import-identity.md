---
date: '2023-09-01'
title: "Import Interoperability Identity Endpoint"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-import-identity
    parent: corda5-interop-admin
    weight: 5000
section_menu: corda5
---

# Import Interoperability Identity Endpoint

You can use the `importInterOpIdentity` endpoint to import an Interoperability identity which was previously exported
from elsewhere into the system of another Interoperability identity. This allows for reliable delivery of messages between
the Interoperability identities as the information of identity you wish to interoperate with will now be available to call
from flow level. It also enables the same level of authentication between identities as they would have between peers and
the application network.

The endpoint is invoked by calling the `GET` method on `/interop/{holdingIdentityShortHash}/import/identity` where the
`holdingIdentityShortHash` is the short hash of the holding identity of the virtual node into which the Interoperability identity will be imported.

It returns a response entity with the status of the request.

Request body example:

```json
{
  "groupPolicy": {
    "fileFormatVersion": 1,
    "groupId": "13fae7c9-a234-4a7a-8613-375d663b158f",
    "p2pParameters": {
      "protocolMode": "Authenticated_Encryption",
      "sessionPki": "Standard",
      "sessionTrustRoots": [
          "-----BEGIN CERTIFICATE-----\\nMIIFKTCCBBGgAwIBAgISBPBWAQX74sKyWaxrwN9Wyf/4MA0GCSqGSIb3DQEBCwUA\\nMDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQD\\nEwJSMzAeFw0yMjA1MTMxMTE0NTlaFw0yMjA4MTExMTE0NThaMBQxEjAQBgNVBAMT\\nCWNvcmRhLm5ldDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMqmvfMO\\nna/+r0V3d3hpGPz5hesAAJRZjJCjsQr5ly8LodIfcPRSz+p5N8ui6ct8lyOmGLmi\\nVzKn6h+On4ilNnd2inIqBRcyFlU4YFyBqq9+FZdR64gEr2CVX8xDz5bMFymLZJoC\\nDnKgzq6LAvhQv/2NIkSRuLI09phKhMwQkAzFaOx0Q1kkmNnJYSf81dF1lbTVAAEH\\nsxMK+4dGECQCYFsfkrpk4wVBnaIdr7JLsrOHbbdLK8Ks/TxVNw20FOvuKZzR28lF\\nZ2roWY7S3s+x6mNZk4zhmTkBFXR747q7IVqj+Un3BU2G5/2TZ6LCJ+8m3WPD+9gz\\nMHdfNwDftNqTuMkCAwEAAaOCAlUwggJRMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUE\\nFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQU\\ntd2w7gkV6EYKUVTrXLPbKNpIc1UwHwYDVR0jBBgwFoAUFC6zF7dYVsuuUAlA5h+v\\nnYsUwsYwVQYIKwYBBQUHAQEESTBHMCEGCCsGAQUFBzABhhVodHRwOi8vcjMuby5s\\nZW5jci5vcmcwIgYIKwYBBQUHMAKGFmh0dHA6Ly9yMy5pLmxlbmNyLm9yZy8wIwYD\\nVR0RBBwwGoIJY29yZGEubmV0gg13d3cuY29yZGEubmV0MEwGA1UdIARFMEMwCAYG\\nZ4EMAQIBMDcGCysGAQQBgt8TAQEBMCgwJgYIKwYBBQUHAgEWGmh0dHA6Ly9jcHMu\\nbGV0c2VuY3J5cHQub3JnMIIBBgYKKwYBBAHWeQIEAgSB9wSB9ADyAHcA36Veq2iC\\nTx9sre64X04+WurNohKkal6OOxLAIERcKnMAAAGAvVf0zgAABAMASDBGAiEA7LTc\\nKcc22HaRFQBqt5zCQjdUcuuZCzbDuhYfL7zbeW4CIQC/Jw3uq7nj1XjpPVb8amYO\\nZBaIyLtqvfdLpnSvIe+NowB3ACl5vvCeOTkh8FZzn2Old+W+V32cYAr4+U1dJlwl\\nXceEAAABgL1X9L0AAAQDAEgwRgIhALp82uqQgsTTSGoQ44obZdgin8eLrUb0fnJX\\nuiOEjeIMAiEA4GM7LhToVLb7+EtEoCtkH7Mwr8rsmTV9oXYzjXuWUfQwDQYJKoZI\\nhvcNAQELBQADggEBAHMyXmq77uYcC/cvT1QFzZvjrohxeZQHzYWsIho6DfpS8RZd\\nN+O1sa4/tjMNN5XSrAY7YJczgBue13YH+Vw9k8hVqJ7vHKSbFbMrF03NgHLfM2rv\\nCHPCZCv3zqESdkcNaXNYDykcwpZjmUFV8T2gy8se+3FYfgiDr6lfpUIDF47EaD9S\\nIFv3D2+FNNS2VaC2U2Uta1XQkrdkUznq8A4rTY3RTTjlMhXf2OP19eUqsmFKF+5D\\nfMTdCNm5Klag/h/ogvYRXxYFvr+4l5hOzK1IJJWoftGi4s1f1pgv/sbi2DXKNPOP\\n7oKylBF5li7LtauuKA6rZM3S62LJvt/Y+d5mgaA=\\n-----END CERTIFICATE-----\\n"
      ],
      "tlsPki": "Standard",
      "tlsTrustRoots": [
          "-----BEGIN CERTIFICATE-----\\nMIIFHjCCBAagAwIBAgISAy1ybKW9u73QQxLAktLHTEQQMA0GCSqGSIb3DQEBCwUA\\nMDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQD\\nEwJSMzAeFw0yMjA1MTExNTAxMDZaFw0yMjA4MDkxNTAxMDVaMBExDzANBgNVBAMT\\nBnIzLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMqmvfMOna/+\\nr0V3d3hpGPz5hesAAJRZjJCjsQr5ly8LodIfcPRSz+p5N8ui6ct8lyOmGLmiVzKn\\n6h+On4ilNnd2inIqBRcyFlU4YFyBqq9+FZdR64gEr2CVX8xDz5bMFymLZJoCDnKg\\nzq6LAvhQv/2NIkSRuLI09phKhMwQkAzFaOx0Q1kkmNnJYSf81dF1lbTVAAEHsxMK\\n+4dGECQCYFsfkrpk4wVBnaIdr7JLsrOHbbdLK8Ks/TxVNw20FOvuKZzR28lFZ2ro\\nWY7S3s+x6mNZk4zhmTkBFXR747q7IVqj+Un3BU2G5/2TZ6LCJ+8m3WPD+9gzMHdf\\nNwDftNqTuMkCAwEAAaOCAk0wggJJMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAU\\nBggrBgEFBQcDAQYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUtd2w\\n7gkV6EYKUVTrXLPbKNpIc1UwHwYDVR0jBBgwFoAUFC6zF7dYVsuuUAlA5h+vnYsU\\nwsYwVQYIKwYBBQUHAQEESTBHMCEGCCsGAQUFBzABhhVodHRwOi8vcjMuby5sZW5j\\nci5vcmcwIgYIKwYBBQUHMAKGFmh0dHA6Ly9yMy5pLmxlbmNyLm9yZy8wHQYDVR0R\\nBBYwFIIGcjMuY29tggp3d3cucjMuY29tMEwGA1UdIARFMEMwCAYGZ4EMAQIBMDcG\\nCysGAQQBgt8TAQEBMCgwJgYIKwYBBQUHAgEWGmh0dHA6Ly9jcHMubGV0c2VuY3J5\\ncHQub3JnMIIBBAYKKwYBBAHWeQIEAgSB9QSB8gDwAHYAKXm+8J45OSHwVnOfY6V3\\n5b5XfZxgCvj5TV0mXCVdx4QAAAGAs9o+JQAABAMARzBFAiEAi07Xbw6nqHBtGQzN\\nLXbCPx68E2xYa9M/ytztzJb96IYCIAiIc9y7u2H510F8AQ1zon7wDQjaTTvL3Ezl\\nJBgFK02aAHYAQcjKsd8iRkoQxqE6CUKHXk4xixsD6+tLx2jwkGKWBvYAAAGAs9o+\\nZwAABAMARzBFAiEAyO7PeW40ocwt+QqSMZAJHKRe7Ip1kYkjUhabhVQD0CoCIBpD\\nqJEJd3UlGIUyxJ44i72xQ6kvn5adfnmJE5Jh8YwPMA0GCSqGSIb3DQEBCwUAA4IB\\nAQBRENd2mg7C73zwxAduIDcYaQ+bKaM9+edHBC+h7cDSACdQ1J+AKruWWYOfQJXG\\nQvudeDU2W7+kUC/0fq0Ui9cGCQBY+EacFN6261z2jVLtdGwJWRe2pYwIVOdknFet\\nMY31Fqih/HToiaX1Fz0qkN0TrdLBsMIZEx3XAiMHbJH4AOrr+V2FpV6GIAZ1A68I\\nFkR4W6zPnI7cwjpeLnO6x1A92y5txtNBeBu0DDnbt695J8BVZeJBei0gIVe3y1Xf\\n2xPJfCYMCpysD6ADGOmMrahZ4ANfDck27hIDw8GXYDBp8XP7teM7r/OVRJW5MJUK\\nxcTyC7ANrJ7GGChxJZUaq0Qu\\n-----END CERTIFICATE-----\\n"
      ],
      "tlsType": "OneWay",
      "tlsVersion": "1.3"
    }
  },
  "members": [
    {
      "endpointProtocol": "1",
      "endpointUrl": "<https://corda-p2p-gateway-worker.corda:8080>",
      "facadeIds": [
        "org.corda.interop/platform/tokens"
      ],
      "owningIdentityShortHash": "1750C7ECD7B4",
      "x500Name": "O=Gold, L=London, C=GB"
    }
  ]
}
```
