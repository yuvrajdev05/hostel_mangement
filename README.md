# Hostel Management System

A portable hostel management application that automatically adapts to available storage systems (MySQL or CSV files).

## Features

- **Automatic Storage Detection**: Uses MySQL if available, otherwise falls back to CSV files
- **User Authentication**: Admin and Student roles with different access levels
- **Student Management**: Add, view, update, and delete student records
- **Room Management**: Manage room information and occupancy
- **Data Export**: Export data to CSV and PDF formats
- **Dashboard**: Overview of key metrics
- **Portable**: Runs on any system with Python

## Quick Start

### Option 1: One-Click Run (Recommended)
```bash
python run.py
```
This script will automatically:
- Check for required dependencies
- Install missing packages
- Start the application

### Option 2: Manual Setup
```bash
# Install dependencies
pip install pandas

# Optional dependencies for enhanced features
pip install mysql-connector-python reportlab

# Run the application
python app.py
```

## Default Credentials

- **Admin**: username=`admin`, password=`admin123`
- **Student**: username=`student1`, password=`student123`

## Storage Options

### MySQL Database (Preferred)
- Automatically detected if MySQL is available on localhost
- Database: `hostel_management`
- Default connection: `root:root@localhost`

### CSV Files (Fallback)
- Used when MySQL is not available
- Data stored in `data/` directory
- Files: `users.csv`, `students.csv`, `rooms.csv`

## File Structure

```
hostel_management/
├── app.py              # Main tkinter GUI application
├── storage.py          # Storage manager (MySQL/CSV)
├── run.py              # Standalone runner script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── data/              # CSV storage directory (auto-created)
    ├── users.csv
    ├── students.csv
    └── rooms.csv
```

## Features by Role

### Admin Features
- Dashboard with key metrics
- Complete student management (CRUD operations)
- Room management
- Data export (CSV/PDF)

### Student Features
- View personal details
- Check room assignment
- View check-in status

## System Requirements

- Python 3.7 or higher
- Internet connection (for initial dependency installation)
- Optional: MySQL server for database storage

## Deployment

This application is designed to be portable. Simply copy the entire folder to any system with Python and run:

```bash
python run.py
```

The application will automatically adapt to the available storage system and install required dependencies.

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL server is running
- Check connection credentials in `storage.py`
- Application will automatically fall back to CSV storage

### Missing Dependencies
- Run `python run.py` to auto-install dependencies
- Or manually install: `pip install streamlit pandas`

### GUI Issues
- Application runs as a desktop GUI using tkinter
- No web browser required

## Data Persistence

- **MySQL**: Data persists in database
- **CSV**: Data stored in local `data/` directory
- Exports saved in application root directory

## Security Notes

- Change default passwords in production
- For MySQL: Update connection credentials
- For CSV: Secure the `data/` directory appropriately