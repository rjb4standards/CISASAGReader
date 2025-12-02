# CISASAGReader
Python app to read and automate the processing of CISA Software Acquisition Guide Spreadsheets based on CISA format https://cisa.gov/sag

The CISASAGReader product may also serve as a *role model* for what a Secure by Design solution *should* provide to satisfy the Secure by Design transparency principle by providing consumers with artifacts to enable a comprehensive software risk assessment, such as an SBOM, living Vulnerability Disclosure Report (VDR), Vendor Response File (VRF) listing additional company information and SDLC policy and product details (i.e. Support Status and Commercial Status), and the CISA Software Acquisition Guide Spreadsheet completed by the software producer. **A final risk assessment report of the CISASAGReader open-source product is available on request, per the EU-CRA requirements** [via e-mail with the subject line "Request for CISASAGReader Risk Assessment Final Report"](mailto:dick@businesscyberguardian.com)

[What does it mean to be "Secure by Default" and "Secure by Design" based on CISA Guidance](https://www.linkedin.com/posts/richard-dick-brooks-8078241_when-people-ask-me-what-does-it-mean-for-activity-7279899394475192322-es0a?utm_source=share&utm_medium=member_desktop)

Could this group of artifacts provided with the CISASAGReader open-source product (see tble below) also serve as a model for what ***Open Source Stewards*** should provide to satisfy EU-CRA expectations for transparency and Secure by Design/Default?

This README document along with the other artifacts listed in the table below aim to satisfy the set of technical documentation cited in Article 31 and the EU CRA **"Declaration of Conformity"** expectations requried by [EU-CRA Annex VII](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_VII)

The SCRM practices implemented during the creation of this product followed the Supply Chain Risk Management (SCRM) implementation guidance provided by the US National Aeronatutics and Space Administration [NASA SCRM Guidance Materials](https://www.nasa.gov/secure-software-development-self-attestation-resources-and-knowledge/)

## How long did it take to produce the CISASAGReader SBOM, VDR, VRF and CISA Software Acquistion Guide Spreadsheet Attestation Artifacts?

| **Artifact**   | **Duration** | **Tool Used** |  
|:----------:|:-----:| -------------------:
| [Software Bill of Materials - SBOM](https://raw.githubusercontent.com/rjb4standards/CISASAGReader/refs/heads/main/CISASAGReader-V1_0_4-SBOM.json) | 10 minutes | sbom4python |
| [Vulnerability Disclosure Report - VDR](https://raw.githubusercontent.com/rjb4standards/CISASAGReader/refs/heads/main/CISASAGReader-V1_0_4-VDR.json) | 15 minutes | SAG-PM and [open source VDR schema](https://raw.githubusercontent.com/rjb4standards/REA-Products/refs/heads/master/SAGVulnDisclosure.xsd) |
| [Vendor Response Form - VRF](https://raw.githubusercontent.com/rjb4standards/CISASAGReader/refs/heads/main/CISASAGReader-VRF.json) | 45 minutes | notepad++ and [open source VRF schema](https://raw.githubusercontent.com/rjb4standards/REA-Products/refs/heads/master/SAGVendorSchema.xsd)|
| [CISA SAG Spreadsheet](https://github.com/rjb4standards/CISASAGReader/raw/refs/heads/main/CISASAGReader-spreadsheet.xlsx) | 50 minutes | Excel |
| [CISA Secure Software Attestation Form - DOE Version](https://github.com/rjb4standards/CISASAGReader/blob/main/CISASAGReader-Attestation-Form.pdf) | 25 minutes | Adobe Acrobat |

Registering the [Trust Label](https://softwareassuranceguardian.com/SAGCTR_inquiry/getTrustedProductLabel?ProductID=3CFC1693E63CE1D3D85C6853C1F1460C94A48BB4CC48DADDC7F067563F9A5A28&html=1) with a "Trust Score" in the SAG-CTR(TM) product **Trust Registry** required a risk assessment and evaluation of the RA results ( 90 minutes ) due to the small size of CISASAGReader and no reported vulnerabilities. It's also imperative that people understand the differences between a "Risk Score" and a "Trust Score", [they are very different concepts](https://energycentral.com/c/um/understanding-difference-between-risk-scores-and-trust-scores). The IETF is working on a standard "Trust Registry" protocol within the Supply Chain Integrity, Transparency and Trust work group [SCITT](https://datatracker.ietf.org/doc/draft-ietf-scitt-software-use-cases/)

## Installation
You may use `pip` or `pipx` (https://pipx.pypa.io/stable/) to install the CISASAGReader.

We recommend installing it with `pipx` for ease of use after installation.

Simply run
```sh
pipx install sag-reader
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

## Miscellaneous

### Trust Label lookup using: curl -s https://softwareassuranceguardian.com/labellink/getTrustedProductLabel?ProductID=3CFC1693E63CE1D3D85C6853C1F1460C94A48BB4CC48DADDC7F067563F9A5A28

### SAGSCore Trust Label: https://softwareassuranceguardian.com/SAGCTR_inquiry/getTrustedProductLabel?ProductID=3CFC1693E63CE1D3D85C6853C1F1460C94A48BB4CC48DADDC7F067563F9A5A28&html=1 

SBOM: Implements [SPDX Version 2.3](https://spdx.github.io/spdx-spec/v2.3/) in JSON format

VDR: Implements [open-source VDR schema](https://raw.githubusercontent.com/rjb4standards/REA-Products/refs/heads/master/SAGVulnDisclosure-V212.xsd) using JSON output format

VRF: Implements [open source VRF schema](https://raw.githubusercontent.com/rjb4standards/REA-Products/refs/heads/master/SAGVendorSchema.xsd) using JSON output format

CISA Secure Software Attestation Form implements [DOE Secure Software Form F 205.2](https://www.energy.gov/cio/doe-f-2052-secure-software-development-attestation) in PDF format

SAG Spreadsheet: Implements [CISA Software Acquisition Guide spreadsheet](https://cisa.gov/sag) in Excel format

When people ask me how to check that a vendor/product is following CISA Secure by Design principles and practices, [**here is what I tell them**](https://www.linkedin.com/posts/richard-dick-brooks-8078241_when-people-ask-how-to-i-check-that-a-software-activity-7273376285282783233-NVJx?utm_source=share&utm_medium=member_desktop). People looking for a good model to procure trustworthy software products should consider this [procurement guidance from NASA](https://energycentral.com/c/iu/caveat-emptor-software-consumers-has-arrived)

Here is a simple windows batch file to process all SAG Spreadsheets in a folder
```sh
REM Requires variable expansion to be enabled cmd /V
@echo off
setlocal

set "ResultFile=SAGresults.txt"
set "folder_path=C:\users\dick\SAGSPDfiles"
for %%f in (%folder_path%\*) do ( 
echo "PROCESSING FILE: " %%f
pause  
call sag-reader --include-descriptions %%f 
set /P "PassFail=Pass or Fail?"
echo %%f,!PassFail!, %DATE%, %TIME% >> %ResultFile%)
echo Results are stored in: %ResultFile%

```
