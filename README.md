# Nuvana Bank Portal

A comprehensive banking portal built with Python and Streamlit.

## Features

- User Authentication & Security
- Dashboard with Account Summary
- Transaction Management
- Loan Management with EMI Calculator
- User Profile & Settings
- Security Features
- Admin Panel
- Reporting & Export
- Help & Support

## Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/nuvana-bank-portal.git
cd nuvana-bank-portal
\`\`\`

2. Install the required dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Run the application:
\`\`\`bash
streamlit run main.py
\`\`\`

## Requirements

- Python 3.11+
- Streamlit
- Pandas
- Matplotlib
- Plotly
- PyOTP
- Other dependencies listed in requirements.txt

## Project Structure

\`\`\`
banking_portal/  
├── main.py  
├── data/  
│   ├── users/  
│   ├── sessions/  
│   └── logs/  
├── utils/  
│   ├── auth.py (login logic)  
│   ├── db.py (JSON read/write)  
│   └── security.py (hashing/OTP)  
├── pages/  
│   ├── dashboard.py  
│   ├── transactions.py  
│   ├── loans.py  
│   ├── settings.py  
│   ├── admin.py  
│   └── help.py  
├── assets/  
│   ├── css/  
│   └── images/ (logos, icons)  
└── README.md
\`\`\`

## Usage

### User Accounts

For demo purposes, you can register a new account or use the following test accounts:

- Regular User:
  - Email: user@example.com
  - Password: password123

- Admin User:
  - Email: admin@example.com
  - Password: admin123

### Admin Panel

The admin panel is only accessible to users with the "admin" role. It provides functionality for:

- User Management
- Loan Approval
- Transaction Monitoring

## Security Features

- Password hashing
- Two-factor authentication
- Session management
- Input validation
- Atomic file operations

## Data Storage

All user data is stored in JSON files in the `data/users/` directory. Each user has a unique JSON file named with their user ID.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Streamlit for the amazing web framework
- The Python community for the excellent libraries
