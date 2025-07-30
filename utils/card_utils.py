def detect_card_brand(card_number):
    if card_number.startswith("4"):
        return "visa"
    elif card_number[:2] in ["51", "52", "53", "54", "55"]:
        return "mastercard"
    elif card_number.startswith("34") or card_number.startswith("37"):
        return "amex"
    return "unknown"
