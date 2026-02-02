# Student Analytics Dashboard
Streamlit-based student analytics dashboard

## 1. Install Libraries
Run this in the **first cell** in Google Colab:

```bash
!pip install streamlit plotly pandas openpyxl --quiet
!npm install -g localtunnel --quiet
print("✅ Libraries installed!")


## 2.Upload Dataset
Upload your dataset (Excel/CSV) to Colab.

3. Run app.py
Run the app in cell 2:

python
# Clone the repository or upload app.py
!wget -O app.py https://raw.githubusercontent.com/your-repo/app.py
4. Run Setup Code
Run this in another cell:

bash
# 1. Kill any existing Streamlit process
!fuser -k 8501/tcp

# 2. Get your IP (copy this for the password page)
!curl ipv4.icanhazip.com

# 3. Run the app
!streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false & npx localtunnel --port 8501
5. Access the Dashboard
Open the URL provided by localtunnel

Enter the IP address shown in step 2

The dashboard will appear
