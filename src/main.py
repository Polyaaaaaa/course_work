from src.services import get_operations_dict


def main():
    transactions = get_operations_dict("..\\data\\operations.xls")
    user_date = input("Введите пожалуйста вашу дату в таком формате: 'YYYY:MM:DD HH:MM:SS'")

