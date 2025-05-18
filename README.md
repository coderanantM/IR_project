```markdown
# SmartShop: Intelligent Product Search & Recommendations

[![GitHub stars](https://img.shields.io/github/stars/coderanantM/IR_project?style=social)](https://github.com/coderanantM/IR_project)

SmartShop is a Django-based e-commerce aggregator that provides intelligent product search, personalized recommendations, and modern user experience features including voice input, location awareness, and robust order management.

---

## 🚀 Features

- **Unified Product Aggregation:** Scrapes and integrates data from Amazon, Flipkart, Myntra, Nykaa, and more.
- **Intelligent Search:** Full-text and fuzzy search with typo tolerance and live autocomplete.
- **Advanced Filtering:** Filter by price range, category, delivery time, and more.
- **Personalized Dashboard:**
  - **Pick Where You Left Off:** See products from your recent searches.
  - **Categories to Explore:** Recommendations based on your most frequently searched products.
- **Voice Integration:** Update your profile and address using voice commands (Web Speech API + NLP extraction).
- **Location Awareness:** Auto-detects your location for delivery estimation.
- **Order Management:** Place orders directly from search results, track them in "My Orders".
- **Secure User Authentication:** Django’s built-in authentication, profile management, and password reset via email/OTP.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (easy to migrate to PostgreSQL)
- **Web Scraping:** Requests, BeautifulSoup, Pandas
- **NLP for Voice:** Custom Python utilities
- **Hosting:** AWS

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip

### Steps

```
# Clone the repository
git clone https://github.com/coderanantM/IR_project.git
cd IR_project

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Import sample data (example)
python manage.py import_csv data/mobiles.csv --main_category Electronics --sub_category "Mobile Phones"

# Start the development server
python manage.py runserver
```

---

## 🗂️ Project Structure

```
IR_project/
├── products/          # Product/category models, import scripts, views
├── recommendations/   # Search history, recommendation logic
├── users/             # Authentication, profile, voice/NLP utilities
├── data/              # Sample CSVs from scraping
├── templates/         # HTML templates (search, dashboard, profile, etc.)
├── static/            # Static files (CSS, JS)
└── smartshop/         # Django project config
```

---

## ⚡ Usage

- **Register/Login:** Create an account or log in.
- **Search:** Use the search bar for products, with autocomplete and typo-tolerance.
- **Filter:** Set min/max price, category, and delivery filters.
- **Voice Profile Update:** On your profile, click the microphone icon and speak your preferences (e.g., "Men, 5.5 feet, relaxed fit, 55kg").
- **Personalized Dashboard:** See "Pick Where You Left Off" and "Categories to Explore" based on your activity.
- **Order Products:** Place orders directly from product cards.
- **Track Orders:** View all your orders in "My Orders".

---

## 📋 Key Code Files

- `products/management/commands/import_csv.py` – Flexible CSV import for all categories.
- `search/views.py` – Fuzzy search, filtering, autocomplete.
- `recommendations/models.py` – User search history, recommendation logic.
- `dashboard/views.py` – Personalized dashboard logic.
- `users/nlp_utils.py` – Voice/NLP processing for profile.
- `users/forms.py` – Registration, profile, password reset forms.

---

## 🤝 Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add a feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---

## 👤 Authors

- Anant Malhotra(2022A7PS0182P)
-Richie Singh(2022A7PS0073P)
-Garvit Saini(2022B4TS1515P)

---

## 🔗 Project Link

[https://github.com/coderanantM/IR_project.git](https://github.com/coderanantM/IR_project.git)
```

---

1) Dashboard page
   ![Dashboard homepage](https://github.com/user-attachments/assets/e44816db-bd96-490a-afd5-84629d4539b5)
2) Profile section
   ![PROFILE](https://github.com/user-attachments/assets/a745bbda-13f1-4b1e-a529-60676d3de165)
3) Categories section
   ![Categories section](https://github.com/user-attachments/assets/6fb1a24e-69f3-4d69-9ac7-82c4cd510540)
4) Orders section
   ![Orders section](https://github.com/user-attachments/assets/236726cc-ce9e-44a1-acb8-b448067441f9)
 


 
