import logging
import json
import re


def find_string(operations: list, search_bar: str) -> list:
    """
    функция поиска операций с определенными словами в описании
    """
    result = []
    pattern = re.compile(search_bar, re.IGNORECASE)
    for transaction in operations:
        if pattern.search(transaction["description"]):
            result.append(transaction)
    return result
