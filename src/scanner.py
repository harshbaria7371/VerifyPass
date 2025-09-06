import pandas as pd
import os

def process_scan(coupon_id):
    """
    Processes a scanned QR code (coupon_id) and updates the coupon status.
    :param coupon_id: The unique ID string from the QR code.
    :return:
    """

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    coupons_file = os.path.join(data_dir, 'coupons.csv')

    try:
        # Load coupon data
        coupons_df = pd.read_csv(coupons_file)
    except FileNotFoundError:
        print("Error: coupons.csv not found. Please run qr_generator.py first.")
        return

    # Find the coupon in the DataFrame
    coupon_row = coupons_df[coupons_df['coupon_id'] == coupon_id]

    if coupon_row.empty:
        print("🔴 Invalid QR Code. Coupon ID not found.")
        return

    idx = coupon_row.index[0]
    status = coupons_df.loc[idx, 'status']
    scans_used = coupons_df.loc[idx, 'scans_used']
    valid_scans = coupons_df.loc[idx, 'valid_scans']

    # --- Validation Logi ---
    if status == 'void':
        print(f"❌ Coupon already voided. Total scans used: {scans_used}.")
        return

    if scans_used < valid_scans:
        # Successful scan
        coupons_df.loc[idx, 'scans_used'] += 1
        print("✅ Scan successful! Enjoy your food.")

        # Re-check status to see if it's the final scan
        if coupons_df.loc[idx, 'scans_used'] == valid_scans:
            coupons_df.loc[idx, 'status'] = 'void'
            print("❗ This was the final scan. Coupon status updated to 'void'.")

    else:
        # Scan limit exceeded
        print(f"❌ Scan limit exceeded. Coupon is now void. Scans used: {scans_used}.")
        coupons_df.loc[idx, 'status'] = 'void'

    # Save the updated DataFrame back to the CSV file
    coupons_df.to_csv(coupons_file, index=False)
    print("Database updated.")

def main_scanner_interface():
    print("Welcome to the Food Coupon Scanner.")
    print("Enter 'exit' to exit.")
    while True:
        scanned_id = input("Enter coupon Id (from QR code): ")
        if scanned_id.lower() == 'exit':
            break
        process_scan(scanned_id)
        print("-"*30)

if __name__ == '__main__':
    main_scanner_interface()