# Quick Start Guide

## Getting Started

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Access the Application
Open your browser and navigate to: **http://127.0.0.1:8000**

### 3. Login with Demo Accounts

The application comes with pre-configured demo accounts:

#### Root User (Full Access)
- **Username:** `root`
- **Password:** `root123`
- **Access:** All companies, all features

#### Admin User (Company Admin)
- **Username:** `admin`
- **Password:** `admin123`
- **Company:** Sample Company
- **Access:** Own company data, upload, user management

#### User1 (View Only)
- **Username:** `user1`
- **Password:** `user123`
- **Company:** Sample Company
- **Access:** View own company data only

## Features Overview

### 📊 Dashboard
- View total records, companies, and recent uploads
- Quick action buttons for common tasks
- Recent activity feed

### 📤 Upload CSV
- Drag-and-drop file upload
- Real-time validation
- Format requirements guide
- Upload history

### 📋 View Data
- Searchable and filterable attendance records
- Mobile card view and desktop table view
- Edit and delete capabilities (based on role)
- Export to CSV

### 👥 Manage Users
- Create new users
- Assign roles and companies
- Edit user information
- View user status

### 📜 Upload Logs
- Track all CSV uploads
- View success/error metrics
- Detailed error messages

## CSV Upload Format

### Required Columns
- `EP NO` - Employee Number
- `EP NAME` - Employee Name
- `COMPANY NAME` - Company Name
- `DATE` - Date (YYYY-MM-DD)
- `SHIFT` - Shift information
- `OVERSTAY` - Overstay information
- `STATUS` - Status (P, A, PH, -0.5, -1)

### Optional Columns
- `IN`, `OUT` - Time (HH:MM)
- `IN (2)`, `OUT (2)` - Second time entry
- `IN (3)`, `OUT (3)` - Third time entry
- `OVERTIME` - Overtime hours
- `OVERTIME TO MANDAYS` - Overtime conversion

### Sample CSV
A sample CSV file is included: `sample_attendance.csv`

## Design Features

### Color Palette
- **Cream:** #EFECE3 (Background)
- **Light Blue:** #8FABD4 (Secondary elements)
- **Dark Blue:** #4A70A9 (Primary buttons, accents)
- **Black:** #000000 (Text, borders)

### Responsive Design
- **Desktop:** Fixed top navigation with full menu
- **Mobile:** Bottom navigation bar with essential links
- **Tablet:** Adaptive layout with optimized spacing

### UI Components
- Rounded corners (rounded-2xl)
- Card-based layouts
- Icon integration throughout
- Smooth hover transitions
- Focus states for accessibility

## Tips

1. **Duplicate Records:** If you upload a CSV with existing EP NO + DATE combinations, the records will be updated automatically.

2. **Company Access:** Admin users can only see and manage data for their assigned company.

3. **Upload Validation:** The system validates date formats, time formats, and status values before processing.

4. **Mobile Experience:** The app is fully responsive - try it on your phone!

5. **Error Logs:** Check the upload logs page to see detailed error messages if a CSV upload fails.

## Need Help?

- Check the format requirements in the Upload CSV page
- Review the sample CSV file for correct formatting
- Ensure dates are not in the future
- Verify all required columns are present

## Next Steps

1. Try uploading the sample CSV file
2. Explore the data management features
3. Create a new user account
4. Export data to CSV
5. Check the upload logs

Enjoy using the Attendance Management System! 🎉
