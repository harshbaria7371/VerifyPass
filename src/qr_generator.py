import pandas as pd
import qrcode
import uuid
import os

def generate_coupons(num_days=1):
    """
    Generates unique QR codes for each group any day and populates the coupons.csv file
    :param num_days: The number of days the festival runs.
    :return:
    """
    print("Starting QR code generation...")

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    qr_dir = os.path.join(os.path.dirname(__file__), '..', 'qr_codes')

    # Create the qrcodes directory if it doesn't exist
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)

    try:
        # Load user data
        users_df = pd.read_csv(os.path.join(data_dir, 'users.csv'))
    except FileNotFoundError:
        print("No users.csv found. Please create the file as instructed.")
        return

    coupon_list = []

    # Iterate through each user group
    for _, row in users_df.iterrows():
        group_id = row['group_id']
        members = row['members']

        # Generate coupons for each festival day
        for day in range(1, num_days + 1):
            # The coupon_id will be the data encoded in the QR code
            coupon_id = str(uuid.uuid4())

            # Create QR code object
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(coupon_id)
            qr.make(fit=True)

            # Create and save QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            qr_filename = f"QR_{group_id}_Day{day}.png"
            img.save(os.path.join(qr_dir, qr_filename))

            # Append coupon data to our list
            coupon_list.append({
                'coupon_id': coupon_id,
                'group_id': group_id,
                'day': day,
                'valid-scans': members,
                'scans_used': 0,
                'status': 'valid'
            })

        # Create a DataFramew from the list
        coupons_df = pd.DataFrame(coupon_list)

        # Save to CSV file
        coupons_df.to_csv(os.path.join(data_dir, 'coupons.csv'), index=False)

        print(f"Successfully generated {len(coupons_df)} unique coupons.")
        print("QR codes saved in the 'qrcodes' directory.")
        print("Coupon data saved to 'data/coupons.csv'.")

if __name__ == "__main__":
    generate_coupons(num_days=3)