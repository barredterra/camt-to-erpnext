import csv
import typer
from pathlib import Path
from datetime import datetime
from hashlib import blake2b


app = typer.Typer()

HASH_COLUMNS = [
    "Buchungstag",
    "Betrag",
    "Verwendungszweck",
    "Kontonummer/IBAN",
    "BIC (SWIFT-Code)",
]

DESCRIPTION_COLUMNS = [
    "Beguenstigter/Zahlungspflichtiger",
    "Verwendungszweck",
    "Kontonummer/IBAN",
    "BIC (SWIFT-Code)",
    "Glaeubiger ID",
    "Mandatsreferenz",
    "Kundenreferenz (End-to-End)",
    "Valutadatum",
]

OUTPUT_COLUMNS = [
    "Date",
    "Deposit",
    "Withdrawal",
    "Description",
    "Reference Number",
    "Bank Account",
    "Currency",
]


@app.callback()
def callback():
    """
    CAMT-CSV to ERPNext-CSV Converter
    """


@app.command()
def convert(input_path: Path, output_path: Path):
    """Convert CAMT-CSV to ERPNext-CSV.

    Read a CAMT-CSV from `in_path`, convert date, amount and description,
    calculate a transaction id, and write an ERPNext-CSV to `out_path`.
    """
    with open(input_path, "r", encoding="cp1252") as in_file, open(
        output_path, "w", encoding="utf-8"
    ) as out_file:
        reader = csv.DictReader(in_file, delimiter=";", quoting=csv.QUOTE_ALL)
        writer = csv.DictWriter(out_file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in reader:
            writer.writerow(convert_row(row))


def convert_row(row: dict) -> dict:
    signed_amount = float(row["Betrag"].replace(",", "."))
    return {
        "Date": isoformat_date(row["Buchungstag"], "%d.%m.%y"),
        "Deposit": signed_amount if signed_amount > 0 else None,
        "Withdrawal": abs(signed_amount) if signed_amount < 0 else None,
        "Description": dict_to_str(row, DESCRIPTION_COLUMNS),
        "Reference Number": dict_to_hash(row, HASH_COLUMNS),
        "Bank Account": row["Auftragskonto"],
        "Currency": row["Waehrung"],
    }


def dict_to_hash(data: dict, keys: list[str]) -> str:
    blake_hash = blake2b(digest_size=16)
    for key in keys:
        blake_hash.update(data[key].encode("utf-8"))

    return blake_hash.hexdigest()


def dict_to_str(data: dict, keys: list[str]) -> str:
    return "\n".join([f"{key}: {data[key]}" for key in keys if data[key]])


def isoformat_date(date: str, source_format: str) -> str:
    return datetime.strptime(date, source_format).date().isoformat()
