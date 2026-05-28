# 🏠 Indian House Price Predictor (ML App)

A machine learning web application built using **Streamlit** that predicts real estate prices in India based on property features like location, size, amenities, and nearby facilities.

---

## 🚀 Live App
(Add your deployed link here after deployment)



---

## 📌 Project Overview

This project predicts house prices using a trained regression model on Indian housing data.

It takes into account:
- City & locality
- BHK & bathrooms
- Super & carpet area
- Floor details
- Furnishing type
- Amenities (lift, gated society, parking)
- Distance to metro, hospital, school
- Crime rate index

---

## 🧠 Machine Learning Model

- Model Type: Regression (trained on housing dataset)
- Training Data: `data/house_price_dataset_india_12k.csv`
- Encoded Features stored in: `models/model_columns.pkl`
- Final model saved as: `models/house_price_model.pkl`

---

## 📂 Project Structure

indian-house-price-predictor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│ └── house_price_dataset_india_12k.csv
│
├── models/
│ ├── house_price_model.pkl
│ └── model_columns.pkl
│
├── notebooks/
│ └── eda.ipynb



---

 ⚙️ Installation (Run Locally)

### 1. Clone repo

git clone https://github.com/harshitha-n06/indian-house-price-predictor.git
cd indian-house-price-predictor


###2.Create virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


###3. Install dependencies

pip install -r requirements.txt

### 4. Run app

streamlit run app.py







