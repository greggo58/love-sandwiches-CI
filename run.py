import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: '10,11,12,13,14,15'\n")

        data_str = None
        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Input data is valid!")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all strong values into integers.
    Raises ValueError if strings cannot be converted to int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
        [int(value) for value in values]
    except ValueError as e:
        print(f"*** Invalid data: {e}, please try again. ***\n")
        return False
    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from teh stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print (stock_row)
    print("\nSurplus data calculated!")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(val) for val in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to Love Sandwiches Data Automation")
main()
