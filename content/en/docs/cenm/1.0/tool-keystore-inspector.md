+++
date = "2020-01-08T09:59:25Z"
title = "Key store inspector tool"
aliases = [ "/releases/release-1.0/tool-keystore-inspector.html",]
menu = [ "cenm-1-0",]
tags = [ "tool", "keystore", "inspector",]
+++


# Key store inspector tool

The key store inspect tool prints out all the certificate chains stored in the given key store file.


## Usage

```bash
java -jar utilities-<<version>>.jar keystore-inspector --inspectkeystore [options]``
```

## Example

```bash
java -jar utilities-<<version>>.jar \
keystore-inspector \
--inspectkeystore \
--keystore ./keystore.jks \
--password password
```
*–help* prints a list of all the available options.


