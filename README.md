# 💰 Daily Tracker - Income & Expenses Manager

A beautiful, modern web app to track your daily income and expenses. Store data permanently in a SQLite database, export to CSV, and visualize trends with interactive charts.

![Daily Tracker](https://img.shields.io/badge/Python-Flask-blue) ![SQLite](https://img.shields.io/badge/Database-SQLite-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

✅ **Easy-to-use interface** - Add custom earning and expense categories on the fly  
✅ **SQLite database** - Permanent data storage (no data loss)  
✅ **Data export** - Download records as CSV for Excel/Sheets  
✅ **Beautiful charts** - Visualize earnings vs expenses trends using Chart.js  
✅ **Responsive design** - Works perfectly on desktop, tablet, and mobile  
✅ **Real-time summary** - See your financial status instantly  
✅ **Fully free** - No ads, no premium features, no registration needed  

---

## 📸 Screenshots

### Home Page
- Input custom earnings and expenses
- Add/remove categories as needed
- Beautiful gradient UI

### Results Page
- Instant summary of your day
- Color-coded earnings (green) and expenses (red)
- Financial status indicator

### History Page
- View all past records in a table
- Interactive bar chart: Earnings vs Expenses
- Line chart: Net amount trend over time
- Sort and filter capabilities

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/daily-tracker.git
   cd daily-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://127.0.0.1:5000`

---

## 📁 Project Structure

```
daily-tracker/
├── app.py                    # Main Flask application
├── migrate_json_to_sqlite.py # Migration script for legacy JSON data
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration for Render
├── DEPLOYMENT.md             # Step-by-step deployment guide
├── README.md                 # This file
├── static/
│   └── style.css            # Complete styling (no inline CSS!)
├── templates/
│   ├── index.html           # Home page with form
│   ├── results.html         # Daily summary page
│   ├── history.html         # History and charts page
│   └── error.html           # Error page
├── tracker_data.db          # SQLite database (auto-created)
├── tracker_data.csv         # CSV export (auto-generated)
└── tracker_data.json        # Legacy JSON (imported to DB)
```

---

## 📊 Database Schema

### `records` table
- `id` (PRIMARY KEY)
- `date` (TEXT) - Timestamp
- `total_earning` (INTEGER)
- `total_expenses` (INTEGER)
- `net` (INTEGER)
- `created_at` (TIMESTAMP)

### `earnings` table
- `id` (PRIMARY KEY)
- `record_id` (FOREIGN KEY)
- `name` (TEXT)
- `amount` (INTEGER)

### `expenses` table
- `id` (PRIMARY KEY)
- `record_id` (FOREIGN KEY)
- `name` (TEXT)
- `amount` (INTEGER)

---

## 🔄 Data Flow

1. **User Input** → Enter custom earnings/expenses on index.html
2. **Calculate** → Flask processes form data (`/calculate` route)
3. **Save to DB** → `save_record_to_db()` inserts into SQLite
4. **Export CSV** → `export_to_csv()` creates backup
5. **Display Results** → results.html shows summary
6. **History View** → `/history` retrieves all records from DB
7. **Visualize** → Chart.js draws interactive graphs

---

## 🌐 Deployment

### Deploy to Render (Free)

1. Push code to GitHub (public repository)
2. Sign up at [render.com](https://render.com)
3. Connect GitHub account and select this repository
4. Create new Web Service with:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click Deploy!

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.**

Your app will be live at: `https://daily-tracker-xxx.onrender.com`

---

## 🛠️ Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** SQLite (built-in, file-based)
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js (for data visualization)
- **Deployment:** Render.com (free cloud platform)
- **Export:** CSV (Excel-compatible)

---

## 📝 Usage Guide

### Adding Income/Expenses

1. Fill in the category name (e.g., "Freelance Work", "Groceries")
2. Enter the amount in rupees (₹)
3. Click "+ Add Earning" or "+ Add Expense" for more entries
4. Click "Calculate Summary" to save and see results

### Viewing History

1. Click "View History" from any page
2. See all past records in a table
3. View earnings vs expenses chart
4. See net amount trend line chart
5. Hover over charts for detailed values

### Exporting Data

- CSV file is **auto-generated** every time you calculate
- Download from your file system: `tracker_data.csv`
- Open in Excel, Google Sheets, or any spreadsheet app

### Migrating Old Data

If you have old `tracker_data.json` from the command-line version:

```bash
python migrate_json_to_sqlite.py
```

This imports all historical records into the SQLite database.

---

## 🎨 UI Features

- **Gradient background** - Purple to violet gradient
- **Responsive layout** - Works on all screen sizes
- **Color coding** - Green for earnings, red for expenses
- **Status indicator** - Visual feedback on financial health
- **Empty states** - Helpful messages when no data
- **Smooth animations** - Button hover effects, slide-in animations
- **Accessible forms** - Clear labels and input validation

---

## 🔒 Privacy & Security

- ✅ **No cloud data collection** - All data stored locally
- ✅ **No registration needed** - Use immediately
- ✅ **No ads or tracking** - 100% privacy-focused
- ✅ **Open source** - Inspect the code yourself
- ✅ **Encrypted in transit** - HTTPS on Render deployment

---

## 📈 Future Enhancements

- [ ] Budget alerts and notifications
- [ ] Monthly/yearly reports
- [ ] Category-wise spending breakdown
- [ ] Recurring expenses/income
- [ ] Multi-user support with login
- [ ] Dark mode theme
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs as GitHub issues
- Suggest new features
- Submit pull requests with improvements
- Share your feedback

---

## 📄 License

This project is licensed under the **MIT License** - free to use, modify, and distribute.

---

## 🆘 Troubleshooting

### App won't start locally?
```bash
python app.py
# Check for error messages and ensure Flask is installed
```

### Database not being created?
```bash
# Delete old database and start fresh
rm tracker_data.db
python app.py
```

### Charts not showing?
- Ensure you have records in the database
- Check browser console for JavaScript errors
- Try a hard refresh (Ctrl+Shift+R)

### Deployment issues?
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting
- Check Render logs for error messages

---

## 📞 Support

- 📧 Email: contact@example.com
- 🐛 Report issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🙏 Acknowledgments

- **Chart.js** - Beautiful JavaScript charting library
- **Flask** - Lightweight Python web framework
- **Render** - Free cloud hosting platform
- **You** - For using Daily Tracker!

---

**Made with ❤️ for financial awareness**

⭐ Star this repo if you find it useful!

