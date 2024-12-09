# CISASAGReader
Python app to read CISA Software Acquisition Guide Spreadsheets based on CISA format https://cisa.gov/sag

V 1.0.2 SAGSCORE Trust Label: https://softwareassuranceguardian.com/SAGCTR_inquiry/getTrustedProductLabel?ProductID=9429E05DF9DDA377F4CF0359904ED020B2AA67C54E945C8F0DAD84B6FFDF3AB1&html=1

V 1.0.3 SAGSCore Trust Label: https://softwareassuranceguardian.com/SAGCTR_inquiry/getTrustedProductLabel?ProductID=5D60680109AAC8DDEED1DD2D0D709179799E6CDC1C2FF918CD371A26D04079A8&html=1

SBOM: SPDX Version 2.3 in JSON format
VDR: Follows open-source VDR format https://github.com/rjb4standards/REA-Products/blob/master/SAGVulnDisclosure.xsd using JSON output format

The CISASAGReader product also serves as a *role model* for what a Secure by Design solution *should* provide to satisfy the Secure by Design transparency principle by providing consumers with artifacts to enable a comprehensive software risk assessment, such as an SBOM, living Vulnerability Disclosure Report (VDR), Vendor Response File (VRF) listing additional company information and SDLC policy details, and the CISA Software Acquisition Guide Spreadsheet completed by the software producer.

## Installation
You may use `pip` or `pipx` (https://pipx.pypa.io/stable/) to install the CISASAGReader.

We recommend installing it with `pipx` for ease of use after installation.

Simply run
```sh
pipx install sag-reader`
```

## Use
Assuming that you installed the CISASAGReader with `pipx`, running it is as simple as
running `sag-reader` from the command line.

To get information on usage, simply run

```sh
sag-reader --help
```

### Try it out for yourself.
*Download the CISASAGReader spreadsheet here*: https://github.com/rjb4standards/CISASAGReader/raw/refs/heads/main/CISASAGReader-spreadsheet.xlsx

*Run sag-reader to view the CISASAGReader Secure by Design responses in the dowloaded spreadsheet*:

```sh
sag-reader --include-descriptions CISASAGReader-spreadsheet.xlsx
```

## Output
The CISASAGReader will parse Excel files (.xlsx and .xls) in the CISA format. It will remove those answers that the spreadsheet indicates do not have to be answered to reduce overall noise.

Output is human-readable by default. However, the `sag-reader` application can also be used to produce output in a JSON format that may be used in downstream processing, such as automated risk analysis, datalake inclusion for population analysis, or simple inclusion in a database for electronic recall and display. For example:

```sh
sag-reader spreadsheet.xls json
```

JSON output is hierarchical by CONTROL or TASK, then the designator broken up by its components. Leaf values in the resultant tree are the values entered on the spreadsheet.

Descriptions are not included in the JSON output or the human-readable output by default. They may be turned on for the human-readable output, for example:

```sh
sag-reader --include-descriptions spreadsheet.xls
```
