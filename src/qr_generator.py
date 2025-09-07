import pandas as pd
import qrcode
import uuid
import os
import datetime

def read_config():
    """
    Reads configurations from the config.txt file.
    :return:
    """
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.txt')
    try:
        with  open(config_path, 'r') as config_file:
            for line in config_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print("Error: config.txt not fount. Please create the file.")
        return None

def generate_coupons():
    """
    Generates unique QR codes for each group any day and populates the coupons.csv file
    :return:
    """
    global coupons_df
    print("Starting QR code generation...")

    config = read_config()
    if not config:
        return None, None

    try:
        start_date_str = config.get('START_DATE')
        num_days_str = config.get('FESTIVAL_DAYS')

        if not start_date_str or not num_days_str:
            print("Error: START_DATE or FESTIVAL_DAYS not found in config.txt")
            return None, None

        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        num_days = int(num_days_str)

    except (ValueError, TypeError) as e:
        print(f"Error parsing config file: {e}. Please ensure dates are in YYYY-MM-DD format.")
        return None, None

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
        return None, None

    coupon_list = []

    # Iterate through each user group
    for _, row in users_df.iterrows():
        group_id = row['group_id']
        members = row['members']

        # Generate coupons for each festival day
        for day_offset in range(num_days):
            # Create a unique, date-specific coupon ID
            unique_id = str(uuid.uuid4())
            coupon_date = start_date + datetime.timedelta(days=day_offset)
            coupon_date_str = coupon_date.strftime('%Y-%m-%d')

            qr_data = f"{unique_id}|{coupon_date_str}"
            # coupon_id = str(uuid.uuid4())

            # Create QR code object
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create and save QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            qr_filename = f"QR_{group_id}_Day{day_offset + 1}.png"
            img.save(os.path.join(qr_dir, qr_filename))

            # Append coupon data to our list
            coupon_list.append({
                'coupon_id': unique_id,
                'qr_data': qr_data,
                'group_id': group_id,
                'day': day_offset + 1,
                'valid_scans': members,
                'scans_used': 0,
                'status': 'valid',
                'valid_date': coupon_date_str
            })

        # Create a DataFrame from the list
        coupons_df = pd.DataFrame(coupon_list)

        # Save to CSV file
        coupons_df.to_csv(os.path.join(data_dir, 'coupons.csv'), index=False)

        print(f"Successfully generated {len(coupons_df)} unique coupons.")
        print("QR codes saved in the 'qrcodes' directory.")
        print("Coupon data saved to 'data/coupons.csv'.")

    return coupons_df, users_df

def generate_distribution_files(coupons_df, users_df):
    """
    Generates text files for each user group with their QR code details
    :param coupons_df:
    :param users_df:
    :return:
    """
    print("Generating distribution files...")
    distribution_dir = os.path.join(os.path.dirname(__file__), '..', 'distribution_files')
    if not os.path.exists(distribution_dir):
        os.makedirs(distribution_dir)

    # Merge dataframes to get user info alongside coupon info
    merged_df = pd.merge(coupons_df, users_df, on='group_id')

    # Group by email to create a singlee file for each recipient
    for email, group in merged_df.groupby('email'):
        file_path = os.path.join(distribution_dir, f"{group.iloc[0]['group_id']}_coupons.txt")

        with open(file_path, 'w') as f:
            f.write(f"Subject: Your Food Coupons for the Festival \n\n")
            f.write(f"Hello {group.iloc[0]['owner_name']} ({group.iloc[0]['tower']}-{group.iloc[0]['flat_number']}),\n\n")
            f.write(f"Thank you for paying for the festival food. Please find your unique QR codes below.\n")
            f.write(f"Each QR code is valid for **{group.iloc[0]['members']}** scans.\n\n")

            for _, row in group.iterrows():
                qr_filename = f"QR_{row['group_id']}_Day{row['day']}.png"
                f.write(f"Day {row['day']} Coupon:\n")
                f.write(f"  - Coupon ID: {row['qr_data']}\n")
                f.write(f"  - QR Code Image: See attached file '{qr_filename}' or scan the image in the 'qrcodes' folder.\n\n")

    print("Distribution files generated in the 'distribution_files' directory.")

if __name__ == "__main__":
    coupons_df, users_df = generate_coupons()
    if coupons_df is not None and users_df is not None:
        generate_distribution_files(coupons_df, users_df)