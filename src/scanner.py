import pandas as pd
import os
import datetime

def process_scan(qr_data):
    """
    Processes a scanned QR code (coupon_id) and updates the coupon status.
    :param qr_data(str): The unique ID string from the QR code, e.g., "UUID|YYYY-MM-DD".
    :return:
    """

    try:
        coupon_id, coupon_date_str = qr_data.split('|')
        scan_date = datetime.date.today().strftime('%Y-%m-%d')
    except ValueError:
        print("🔴 Invalid QR Code format. Please scan a valid festival QR.")
        return

    if scan_date != coupon_date_str:
        print(f"❌ This coupon is not valid for today, {scan_date}. It is for {coupon_date_str}.")
        return

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
        scanned_id = input("Enter QR code data (e.g.,UUID|YYYY-MM-DD): ")
        if scanned_id.lower() == 'exit':
            break
        process_scan(scanned_id)
        print("-"*30)

if __name__ == '__main__':
    main_scanner_interface()