# CISASAGReader
Python app to read CISA Software Acquisition Guide Spreadsheets based on CISA format https://cisa.gov/sag

## Installation
You may use `pip` or `pipx` (https://pipx.pypa.io/stable/) to install the CISASAGReader.

We recommend installing it with `pipx` for ease of use after installation.

Simply run `pipx install sag-reader`.

## Use
Assuming that you installed the CISASAGReader with `pipx`, running it is as simple as
running `sag-reader` from the command line.

To get information on usage, simple run `sag-reader --help`.

## Output
The CISASAGReader will parse Excel files (.xlsx) in the CISA format. It will remove those answers that the spreadsheet indicates do not have to be answered to reduce overall noise.

Output is human-readable by default. However, the `sag-reader` application can also be used to produce output in a JSON format that may be used in downstream processing, such as automated risk analysis, datalake inclusion for population analysis, or simple inclusion in a database for electronic recall and display.

JSON output is hierarchical by CONTROL or TASK, then the designator broken up by its components. Leaf values in the resultant tree are the values entered on the spreadsheet. 

Descriptions are not included in the JSON output or the human-readable output by default. They may be turned on for the human-readable output.
