# student-analytics-dashboard
Streamlit-based student analytics dashboard

1 Install Libraries in the first cell in google colab
#!pip install streamlit plotly pandas openpyxl --quiet
#!npm install -g localtunnel --quiet
#print("✅ Libraries installed!")
2 upload dataset
3 run app.py in cell 2
4 run this code in another cell
#1. Kill any existing Streamlit process
!fuser -k 8501/tcp

#2. Get your IP (copy this for the password page)
!curl ipv4.icanhazip.com

#3. Run the app
!streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false & npx localtunnel --port 8501
5 copy the address result 
6 open the link 
7 write the address inside the link 

Dashboard will appear
