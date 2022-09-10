import csv
import typer
from pathlib import Path
from datetime import datetime
from hashlib import blake2b


app = typer.Typer()


@app.callback()
def callback():
    """
    CAMT-CSV to ERPNext-CSV Converter
    """


@app.command()
def convert(in_path: Path, out_path: Path):
    """Convert CAMT-CSV to ERPNext-CSV"""
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

    # csv.register_dialect("camt", delimiter=";", quoting=csv.QUOTE_ALL)
    with open(in_path, "r", encoding="cp1252") as in_file:
        reader = csv.DictReader(in_file, delimiter=";", quoting=csv.QUOTE_ALL)
        output = []
        for row in reader:
            signed_amount = float(row["Betrag"].replace(",", "."))

            output.append(
                {
                    "Date": datetime.strptime(row["Buchungstag"], "%d.%m.%y")
                    .date()
                    .isoformat(),
                    "Deposit": signed_amount if signed_amount > 0 else None,
                    "Withdrawal": abs(signed_amount) if signed_amount < 0 else None,
                    "Description": "\n".join(
                        [
                            f"{column}: {row[column]}"
                            for column in DESCRIPTION_COLUMNS
                            if row[column]
                        ]
                    ),
                    "Reference Number": transaction_id(row),
                    "Bank Account": row["Auftragskonto"],
                    "Currency": row["Waehrung"],
                }
            )

    with open(out_path, "w", encoding="utf-8") as out_file:
        OUTPUT_COLUMNS = [
            "Date",
            "Deposit",
            "Withdrawal",
            "Description",
            "Reference Number",
            "Bank Account",
            "Currency",
        ]
        writer = csv.DictWriter(out_file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output)


def transaction_id(row):
    HASH_COLUMNS = [
        "Buchungstag",
        "Betrag",
        "Verwendungszweck",
        "Kontonummer/IBAN",
        "BIC (SWIFT-Code)",
    ]

    transaction_hash = blake2b(digest_size=16)

    for column in HASH_COLUMNS:
        transaction_hash.update(row[column].encode("utf-8"))

    return transaction_hash.hexdigest()
