# ⚡ Electricity Bill Optimizer Web App

A Streamlit-based web application to help users analyze, visualize, and optimize their electricity bills. The app provides insights into monthly consumption trends, personalized savings tips, household comparisons, and next-month bill predictions.

## Features

- **User-Friendly Input:**  
  - Add monthly bills manually, upload a CSV, or use 12 months of sample data.  
  - Option to customize electricity slab rates and fixed charges.  

- **Bill Analysis:**  
  - Calculates average monthly consumption, bills, peak usage, and trends.  
  - Highlights high-consumption months for better cost management.  

- **Interactive Visualizations:**  
  - Bar charts, line plots, and pie charts to visualize monthly consumption, bills, cost per unit, and estimated appliance breakdown.  
  - Color-coded metrics for quick insights.  

- **Savings Recommendations:**  
  - Personalized tips to reduce electricity usage (AC optimization, LED lighting, water heater timer, unplugging devices, regular maintenance).  
  - Estimated potential monthly and yearly savings.  

- **Household Comparison:**  
  - Compare your average consumption with typical households (Small/Medium/Large apartments, Independent House).  
  - Identifies if your usage is above or below average.  

- **Next Month Prediction:**  
  - Predict expected electricity consumption and bill based on recent usage trends.  
  - Best and worst-case scenarios for planning.  

---

## Demo

Sample Dashboard: <img width="1273" height="853" alt="Screenshot 2025-10-05 210205" src="https://github.com/user-attachments/assets/5feea0c3-2127-4be1-9000-052c0ffe830f" />
  

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/electricity-bill-optimizer.git
   cd electricity-bill-optimizer

2. **Install dependencies:**

        pip install -r requirements.txt

- **If requirements.txt is not available, install manually:**

      pip install streamlit pandas numpy plotly


3. **Run the application:**

        streamlit run app.py


4. **Access the app:**

       Open the provided local URL in your browser (usually http://localhost:8501).

   ---

## Usage

- **Input Bills:**
  - Use the sidebar to manually enter monthly bills, upload a CSV, or load sample data.

- **Analyze Bills:**
  - Click "Analyze My Bills" to view consumption trends, key metrics, and visualizations.

- **Savings Tips:**
  - Personalized actionable recommendations with estimated monthly/yearly savings.

- **Comparison:**
  - Compare your consumption with typical household types and see how you stack up.

- **Next Month Prediction:**
  - Predict expected units and bill for the next month using recent trends.
 
---

## CSV File Format (for Upload)
      month,units,amount
      Jan-24,250,1500
      Feb-24,280,1700
      Mar-24,320,2100
  ---

  ## File Structure

      ├── app.py                 # Main Streamlit app
      ├── README.md              # Project documentation
  ---

  ## Notes

  - All calculations are based on user-defined slab rates (default provided).

  - Predictions are based on last 3 months average consumption.

  - Interactive visualizations require an internet connection for Streamlit + Plotly rendering.

  ---

## Credits

- Streamlit – Web framework

- Pandas
 & NumPy
 – Data handling

- Plotly
 – Interactive visualizations

---

## License

- This project is for educational purposes.
