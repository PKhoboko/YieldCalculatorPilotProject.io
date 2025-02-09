from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase_config import supabase
from supabase import create_client, Client






app = Flask(__name__)

# Replace with your Supabase credentials
SUPABASE_URL = "https://eyhrkybcfmxmgxcpvbzk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5aHJreWJjZm14bWd4Y3B2YnprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE5NTc4OTIsImV4cCI6MjA0NzUzMzg5Mn0.ym_CfMBskcliZ-QTRCbS8knE29h_IJhrRwgQEVBpdgA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# User Authentication Route

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Dashboard: CRUD operations
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    

    # Retrieve data from Supabase Table
    data = supabase.table("kukuukk").select("*").execute().data
    data_list = []
    if request.method == 'POST':
        # Add record
        new_data = {
		"Crop": "Maize",
		"Cultivar":"",
		"Ears": request.form['Ears'],
		"Grain mass": request.form['Grain mass'],
		"I/D": 20355,
		"Lat(-)": -130,
		"Long (  )": 130,
		"Moist %": request.form['Moist %'],
		"Planting date": 20250912,
		"Plants / 10m": 20,
		"Point no": 5068750,
		"Province": "Eastern Cape",
		"Row width": request.form['Row width'],
		"Tillers": 12
	}
        
        supabase.table("kukuukk").insert(new_data).execute()
        data = supabase.table("kukuukk").select("*").execute().data
        total_rows = len(data)  # Get total number of rows
        three_percent_rows = int(total_rows * 0.03)  # Calculate 3% of the rows

        # Take the first 3% of the data
        subset_data = data[:three_percent_rows]
        for i in subset_data:
           
            if isinstance(i['Ears'], (int, float)) and isinstance(str(i['Grain mass']).replace(",", "."), (int, float)) \
            and isinstance(str(i['Moist %']).replace(",", "."), (int, float)) and isinstance(str(i['Row width']).replace(",", "."), (int, float)):
                i["yeild"] = (int(str(i['Ears']))*(float(str(i['Grain mass']))*((100-float(str(i['Moist %'])))/(100-12.5)/float(str(i['Row width'])))))*0.95
            else:
                i["yeild"] = 0
        
        return render_template('dashboard.html',data=subset_data)
    total_rows = len(data)  # Get total number of rows
    three_percent_rows = int(total_rows * 0.03)  # Calculate 3% of the rows

        # Take the first 3% of the data
    subset_data = data[:three_percent_rows]
    for i in data:
         if isinstance(i['Ears'], (int, float)) and isinstance(str(i['Grain mass']).replace(",", "."), (int, float)) \
         and isinstance(str(i['Moist %']).replace(",", "."), (int, float)) and isinstance(str(i['Row width']).replace(",", "."), (int, float)):
                i["yeild"] = (int(str(i['Ears']))*(float(str(i['Grain mass']).replace(",", ".")),0)*((100-float(str(i['Moist %']).replace(",", ".")))/(100-12.5)/float(str(i['Row width']).replace(",", "."))))*0.95
         else:
                i["yeild"] = 0
            
    return render_template('dashboard.html',data=data)

@app.route('/delete/<record_id>')
def delete(record_id):
    supabase.table("kukuukk").delete().eq('Point no', record_id).execute()
    flash("Data Deleted", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
