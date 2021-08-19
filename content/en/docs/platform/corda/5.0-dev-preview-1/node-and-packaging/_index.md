---
title: "Node & Packaging"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-node-packaging
    weight: 100
project: corda-5
section_menu: corda-5-dev-preview
---

# Node & Packaging

## cpb

A file with a cpb extension is a Corda package bundle. This contains zero or more cpk files (CLARIFY THIS), plus a MANIFEST.MF and other Corda related information. This file is a Cordapp, and may contain generic information.

This file can be created using the cpi builder CLI tool (speak to Walter for documentation).

The file type is a jar / zip archive.

cpb = corda package bundle, which contains 1 or more cpk files. It represents a cordapp and any associated generic information

## cpi

A file with a cpi extension is a Corda Package Installer. This contains ONE cpb (CLARIFY THIS - I'm not sure we have yet to be honest). This file additionally contains explicit information (e.g. membership group information, identities, etc. CLARIFY) that allows the containing cpb to be deployed to exactly one network.

A cpi file is also cryptographically signed.

This file can be created using the cpi builder CLI tool (speak to Walter for documentation).

The file type is a jar / zip archive.

cpi = corda package installer, which is a cryptographically signed cpb with specific information such as membership and identities that make it unique to ONE network. This is the unit of deployment of a cordapp in corda5.

## cpk

A file with a cpk extension is a Corda package file. This is an OSGi bundle (https://en.wikipedia.org/wiki/OSGi#Bundles / https://docs.osgi.org/specification/osgi.core/8.0.0/), with extra Corda information in the MANIFEST.MF and additional files.

The file type is a jar / zip archive.

cpk = corda package, which is a jar-like file containing workflows or contracts
