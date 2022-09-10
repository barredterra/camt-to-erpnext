This CLI can convert a CAMT CSV file (provided by your bank) into a normal CSV file that can be used for importing **Bank Transactions** into ERPNext.

Usage:

```
camt-to-erpnext convert IN_PATH OUT_PATH
```

### Input format

- Delimiter: `;`
- Quoting: all columns quoted
- Date Format: `28.02.99`
- Number Format: `-1234,56`
- Columns:
    - Auftragskonto
    - Buchungstag
    - Valutadatum
    - Buchungstext
    - Verwendungszweck
    - Glaeubiger ID
    - Mandatsreferenz
    - Kundenreferenz (End-to-End)
    - Sammlerreferenz
    - Lastschrift Ursprungsbetrag
    - Auslagenersatz Ruecklastschrift
    - Beguenstigter/Zahlungspflichtiger
    - Kontonummer/IBAN
    - BIC (SWIFT-Code)
    - Betrag
    - Waehrung
    - Info

### Output format:

- Delimiter: `,`
- Quoting: where necessary
- Date Format: `1999-02-28`
- Number Format: `1234.56`
- Columns:
    - Date

        "Buchungstag" of the input file, converted to ISO-format

    - Deposit

        "Betrag" of the input file (if > 0)

    - Withdrawal

        Absolute "Betrag" of the input file (if < 0)

    - Description

        The following columns of the input file: "Beguenstigter/Zahlungspflichtiger", "Verwendungszweck", "Kontonummer/IBAN", "BIC (SWIFT-Code)", "Glaeubiger ID", "Mandatsreferenz", "Kundenreferenz (End-to-End)", "Valutadatum"

    - Reference Number

        Hash of the following columns of the input file "Buchungstag", "Betrag", "Verwendungszweck", "Kontonummer/IBAN", "BIC (SWIFT-Code)".

    - Bank Account

        "Auftragskonto" of the input file

    - Currency

        "Waehrung" of the input file
