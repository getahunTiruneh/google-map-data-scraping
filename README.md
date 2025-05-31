# 🗺️ Google Map Data Scraping

This project allows users to scrape business details such as name, address, phone number, websites, ratings, and total reviews directly from Google Maps using a simple Streamlit interface. It is especially useful for collecting business leads or contact information based on specific keywords and locations.

---

## 📌 Features

- ✅ Search by **keyword** and **location**
- ✅ Extract business details (name, phone, address, website)
- ✅ Export data as **CSV** or **Excel**
- ✅ Simple and interactive **Streamlit** dashboard
- ✅ Designed to bypass manual scraping from Google Maps

---

## 🚀 Demo

Run the app and search for businesses like:

> Example: `Hotel` in `Addis Ababa`

![Screenshot](docs/demo-screenshot.png) <!-- Optional: Add a screenshot image here -->

---

## 🧰 Technologies Used

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Selenium](https://selenium.dev/)
- [Pandas](https://pandas.pydata.org/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) for web automation

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/getahuntiruneh/google-map-data-scraping.git
cd google-map-data-scraping
```
### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
### 3. Install Required Packages
```bash
pip install -r requirements.txt
```
### Project Structure
```bash
google-map-data-scraping
├── app.py                        # Streamlit front-end
├── data-extractor.py             # Selenium-based data extraction logic
├── output                        # Folder for exported CSV/Excel files
│   └── google_maps_data_hotel_Addis_Ababa.xlsx
├── README.md                     # You're reading it!
└── requirements.txt              # Python dependencies
