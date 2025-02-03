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
def dashboard():
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    

    # Retrieve data from Supabase Table
    data = supabase.table("kukuukk").select("*").execute().data
    data_list = []
    if request.method == 'POST':
        # Add record
        new_data = {
		"Crop": request.form['Crop'],
		"Cultivar":request.form['Cultivar'],
		"Ears": request.form['Ears'],
		"Grain mass": request.form['Grain mass'],
		"I/D": request.form['I/D'],
		"Lat(-)": request.form['Lat(-)'],
		"Long (  )": request.form['Long (  )'],
		"Moist %": request.form['Moist %'],
		"Planting date": request.form['Planting date'],
		"Plants / 10m": request.form['Plants / 10m'],
		"Point no": request.form['Point no'],
		"Province": request.form['Province'],
		"Row width": request.form['Row width'],
		"Tillers": request.form['Tillers']
	}
        
        supabase.table("kukuukk").insert(new_data).execute()
        data = supabase.table("kukuukk").select("*").execute().data
        for i in data:
            data["yield"] = jsonify((i['Ears']*(i['Grain mass']*((100-i['Moist %'])/(100-12.5)/i['Row width'])))*0.95)
       
        
        return render_template('dashboard.html',data=data)
    for i in data:
            data["yeild"] = jsonify((i['Ears']*(i['Grain mass']*((100-i['Moist %'])/(100-12.5)/i['Row width'])))*0.95)
            
    return render_template('dashboard.html',data=data)

@app.route('/delete/<record_id>')
def delete(record_id):
    supabase.table("kukuukk").delete().eq('Point no', record_id).execute()
    flash("Data Deleted", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
