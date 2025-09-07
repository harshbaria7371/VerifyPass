import pandas as pd
import os
from scanner import process_scan

def display_all_coupons():
    """
    Reads and displays the status of all coupons.
    :return:
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    coupons_file = os.path.join(data_dir, 'coupons.csv')

    try:
        coupons_df = pd.read_csv(coupons_file)
        print("\n--- All Coupon Statuses ---")
        print(coupons_df.to_string(index=False)) # Use to_string for better console output
        print("-"*30)
    except FileNotFoundError:
        print("Error: coupons.csv not found. Please run the QR generator first.")

def main_menu():
    """
    Presents the main menu for the volunteer.
    :return:
    """
    while True:
        print("_"*30)
        print("1. Scan a Coupon (Enter Coupon ID)")
        print("2. Check a Specific Coupon's Status")
        print("3. Display All Coupon Statuses")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            coupon_id = input("Enter Coupon ID: ")
            process_scan(coupon_id)
        elif choice == '2':
            coupon_id = input("Enter Coupon ID to check status: ")
            # Use pandas to find the coupon and print its details
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            coupons_file = os.path.join(data_dir, 'coupons.csv')
            try:
                coupons_df = pd.read_csv(coupons_file)
                coupon = coupons_df[coupons_df['coupon_id'] == coupon_id]
                if coupon.empty:
                    print("Coupon ID not found")
                else:
                    print("\n--- Coupon Details ---")
                    print(coupon.to_string(index=False))
                    print("------------\n")
            except FileNotFoundError:
                print("Error: coupons.csv not found. Please run the QR generator first.")
        elif choice == '3':
            display_all_coupons()
        elif choice == '4':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main_menu()