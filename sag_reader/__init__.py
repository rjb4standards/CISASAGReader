"""
Reads, analyzes, and reports on a CISA Software Acquisition Guide.
Copyright 2018-2024 Business Cyber Guardian a Reliable Energy Analytics LLC Compant
Provided under MIT Licensing Terms
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Optional

import pandas
import rich
import typer

APP = typer.Typer()


class Output(StrEnum):
    """Output format."""

    HUMAN = "human"
    JSON = "json"


def check_filename(p: Path) -> Path:
    """Check that the file exists and is a file."""
    if not p.exists():
        raise typer.BadParameter(f"{p} does not exist.")
    if not p.is_file():
        raise typer.BadParameter(f"{p} is not a file.")
    if not p.suffix.lower() in (".xls", ".xlsx"):
        raise typer.BadParameter(f"{p} is not an Excel file.")
    return p


def human_output(df: pandas.DataFrame, include_descriptions: bool):
    """Output the data in a human-readable format."""
    last_section: str = None
    for row in df.itertuples():
        response: str = None
        match row[3]:
            case "Yes":
                response = "[bold bright_green]Yes[/bold bright_green]"
            case "No":
                response = "[bold bright_red]No[/bold bright_red]"
            case "Partial":
                response = "[bold bright_yellow]Partial[/bold bright_yellow]"
            case "N/A":
                response = "[bright_white]N/A[/bright_white]"
            case _ if pandas.isna(row[3]):
                response = "[bold bright_magenta]No Response[/bold bright_magenta]"
        if last_section != (section := row[1].split(".")[1]):
            if last_section is not None:
                typer.confirm("Continue?", abort=True, default=True, prompt_suffix="")
            last_section = section
        line = f"[bright_blue]{row[1]}[/bright_blue]: {response}"
        if include_descriptions:
            line += f"\n\t[grey62]{row[2]}[/grey62]\n"
        rich.print(line)


def json_output(df: pandas.DataFrame):
    """Output the data in a JSON format."""
    output: dict[str, str] = {}
    for row in df.itertuples():
        components = row[1].split(".")
        item = output
        for n in components[:-1]:
            item = item.setdefault(n, {})
        item[components[-1]] = row[3] if not pandas.isna(row[3]) else None
    print(json.dumps(output, separators=(",", ":")))


@APP.command()
def read_sag(
    filename: Annotated[
        Path,
        typer.Argument(
            callback=check_filename,
            help="Path to the CISA Software Acquisition Guide Spreadsheet.",
            show_default=False,
        ),
    ],
    output: Annotated[
        Optional[Output],
        typer.Argument(
            help="Output format.",
        ),
    ] = Output.HUMAN,
    include_descriptions: Annotated[
        bool, typer.Option(help="Add descriptions to human output.", show_default=True)
    ] = False,
):
    """Read a CISA Software Acquisition Guide."""
    with filename.open("rb") as f:
        sag = pandas.read_excel(
            f,
            keep_default_na=False,
            na_values=[""],
            sheet_name="Governance",
            skiprows=11,
            usecols="A,B,C",
        )
        sag.columns = ["A", "B", "C"]
        for sheet_name in (
            "Supply Chain",
            "Secure Development",
            "Secure Deployment",
            "Vulnerability",
        ):
            df = pandas.read_excel(
                f,
                keep_default_na=False,
                na_values=[""],
                sheet_name=sheet_name,
                skiprows=14,
                usecols="A,B,C,D",
            )
            df = df[
                ~df.iloc[:, 3].isin(
                    ["Question skipped", "Move to Next CONTROL Question."]
                )
            ]
            df = df.iloc[:, :-1]
            df.columns = ["A", "B", "C"]
            sag = pandas.concat([sag, df], ignore_index=True)
    if output == Output.HUMAN:
        human_output(sag, include_descriptions)
    else:
        json_output(sag)


def main():
    """Main entry point."""
    APP()
