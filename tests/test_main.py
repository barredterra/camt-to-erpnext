INPUT_DICT = {
    "Buchungstag": "01.01.20",
    "Betrag": "-199,99",
    "Verwendungszweck": "RE Nr. R-2022-0001",
    "Kontonummer/IBAN": "DE12345678901234567890",
    "BIC (SWIFT-Code)": "DEUTDEFFXXX",
}


def test_dict_to_str():
    from camt_to_erpnext.main import dict_to_str

    assert (
        dict_to_str(INPUT_DICT, ["Verwendungszweck", "Kontonummer/IBAN"])
        == "Verwendungszweck: RE Nr. R-2022-0001\nKontonummer/IBAN: DE12345678901234567890"
    )


def test_isoformat_date():
    from camt_to_erpnext.main import isoformat_date

    assert isoformat_date("01.01.20", "%d.%m.%y") == "2020-01-01"


def test_dict_to_hash():
    from camt_to_erpnext.main import dict_to_hash

    assert (
        dict_to_hash(INPUT_DICT, ["Buchungstag", "Betrag"])
        == "b6dc9375b279e8888f2dd5be7cf50843"
    )
