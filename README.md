# VerifyPass
A Python system for secure event pass verification. It generates unique, multi-use QR codes for groups, which are valid for a set number of scans before being automatically voided. The system updates a database in real time, streamlining access control for your event.

### **Key Features**
- **Unique QR Code Generation**: Generates a unique QR code for each group/family for each day of the festival.
- **Dynamic Validity**: Each QR code is valid for a specific number of scans, corresponding to the number of members in the group.
- **Automated Validation**: The system automatically tracks the number of scans and updates a coupon's status to 'void' after its scan limit is reached.
- **Data Management**: Utilizes CSV files for initial data storage and validation, with a clear path for future migration to a secure database.

### **How It Works**
The system is built on two core components:
1.  **`qr_generator.py`**: This script reads user data (`users.csv`) and creates unique coupons for each group. It then populates the `coupons.csv` file, which acts as our central ledger, and saves the QR code images.
2.  **`scanner.py`**: This script simulates a volunteer's scanning app. It takes a unique QR code ID, validates its status against `coupons.csv`, and updates the scan count in real-time.

## **Getting Started**

### **Prerequisites**
- Python 3.9.13 or higher
- `pip` package manager

### **Installation**
1.  Clone this repository to your local machine.
2.  Navigate to the project directory:
    `cd food_coupon_system`
3.  Install the required Python libraries:
    `pip install pandas qrcode[pil]`

### **Usage**
1.  **Generate Coupons**: Navigate to the `src` directory and run the generator script. This will populate your `data` and `qrcodes` directories.
    `cd src`
    `python qr_generator.py`
2.  **Run the Scanner**: Use the main application to validate coupons and view statuses.
    `python main.py`

## ⚠️ Troubleshooting

### 🚧 Common Issues
1. **Initial Data Error**: Double-check your users.csv data is created

### 🐛 Debug Information
- You can enable verbose logging by modifying the print statements in the code.

## 🤝 Contributing
1. **Fork** the repository
2. **Create** a feature branch(`git checkbout -b amazing_feature`)
3. **Commit** your changes
4. **Push** to the branch
5. **Open** a Pull request

## ⚖️ License
This project is licensed under the **MIT License**

## 🙏 Acknowledgments
- Resolve Coupon Distribution issues with Automation knowledge

## 💌 Support 
- Email: bariaharshg@gmail.com 📧
- Issues: [GitHub Issues](https://github.com/harshbaria7371/VerifyPass/issues) 🐛

---
**Made with ❤️**