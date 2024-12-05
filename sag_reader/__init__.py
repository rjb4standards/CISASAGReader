# Copyright 2018-2024 Business Cyber Guardian a Reliable Energy Analytics LLC Compant
# Provided under MIT Licensing Terms
from enum import StrEnum
import json
from pathlib import Path
from typing import Annotated, Optional

import pandas
import typer
from rich import print

APP = typer.Typer()


class Output(StrEnum):
    human = "human"
    json = "json"


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
    for row in df.itertuples():
        response: str = None
        match row[3]:
            case "Yes":
                response = "[bold green]Yes[/bold green]"
            case "No":
                response = "[bold red]No[/bold red]"
            case "Partial":
                response = "[bold yellow]Partial[/bold yellow]"
            case "N/A":
                response = "N/A"
            case _ if pandas.isna(row[3]):
                response = ""
        line = f"[blue]{row[1]}[/blue]: {response}"
        if include_descriptions:
            line += f"\n\t{row[2]}\n"
        print(line)


def json_output(df: pandas.DataFrame):
    output: dict[str, str] = {}
    for row in df.itertuples():
        components = row[1].split(".")
        item = output
        for n in components[:-1]:
            item = item.setdefault(n, {})
        item[components[-1]] = row[3] if not pandas.isna(row[3]) else None
    # print(json.dumps(output, separators=(",", ":")))
    print(json.dumps(output, indent=2))


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
    ] = Output.human,
    include_descriptions: Annotated[
        bool, typer.Option(help="Add descriptions to human output.", show_default=True)
    ] = False,
):
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
    if output == Output.human:
        human_output(sag, include_descriptions)
    else:
        json_output(sag)


def main():
    APP()
