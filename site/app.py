import os
from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import json

app = Flask(__name__, template_folder='templates', static_url_path='/css', static_folder='css')

# Load configuration from config.json
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'config.json')

print(f"Attempting to load configuration from: {CONFIG_FILE_PATH}")

try:
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config_data = json.load(config_file)
        print(f"Successfully loaded configuration: {config_data}")
except Exception as e:
    print(f"Error loading configuration: {e}")
    config_data = {"website_title": "Default Title", "website_name": "Default Name"}


# Define the database file path within the /data folder
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'distilling-tracker.db')

def create_spirits_table():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS spirits (
            batch INTEGER PRIMARY KEY,
            recipe TEXT,
            start_date DATE,
            ingredients TEXT,
            ph TEXT,
            sg TEXT,
            fg TEXT,
            end_date DATE,
            start_time TEXT,
            end_time TEXT,
            distilling_conditioner TEXT,
            litres_distilled TEXT,
            percentage TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_spirits_data():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM spirits')
    data = c.fetchall()
    conn.close()
    return data

create_spirits_table()

@app.route('/')
def index():
    spirits_data = get_spirits_data()
    return render_template('index.html', spirits_data=spirits_data, website_title=config_data['website_title'], website_name=config_data['website_name'])

@app.route('/submit', methods=['POST'])
def submit():
    batch = request.form.get('batch')
    recipe = request.form.get('recipe')
    start_date = request.form.get('start_date')
    ingredients = request.form.get('ingredients')
    ph = request.form.get('ph')
    sg = request.form.get('sg')
    fg = request.form.get('fg')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    distilling_conditioner = request.form.get('distilling_conditioner')
    litres_distilled = request.form.get('litres_distilled')
    percentage = request.form.get('percentage')
    
    if (
        batch and recipe and start_date and ingredients and ph and sg 
    ):
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO spirits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (batch, recipe, start_date, ingredients, ph, sg, fg, end_date, start_time, end_time, distilling_conditioner, litres_distilled, percentage))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:batch>', methods=['GET', 'POST'])
def edit(batch):
    if request.method == 'POST':
        recipe = request.form.get('recipe')
        start_date = request.form.get('start_date')
        ingredients = request.form.get('ingredients')
        ph = request.form.get('ph')
        sg = request.form.get('sg')
        fg = request.form.get('fg')
        end_date = request.form.get('end_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        distilling_conditioner = request.form.get('distilling_conditioner')
        litres_distilled = request.form.get('litres_distilled')
        percentage = request.form.get('percentage')
        
        if (
            recipe and start_date and ingredients and ph and sg and fg and
            end_date and start_time and end_time and distilling_conditioner and
            litres_distilled and percentage
        ):
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute('''
                UPDATE spirits
                SET recipe=?, start_date=?, ingredients=?, ph=?, sg=?, fg=?, end_date=?, 
                start_time=?, end_time=?, distilling_conditioner=?, litres_distilled=?, percentage=?
                WHERE batch=?
            ''', (recipe, start_date, ingredients, ph, sg, fg, end_date, start_time, end_time, distilling_conditioner, litres_distilled, percentage, batch))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM spirits WHERE batch=?', (batch,))
    data = c.fetchone()
    conn.close()
    return render_template('edit.html', data=data, batch=batch, website_title=config_data['website_title'], website_name=config_data['website_name'])

@app.route('/delete/<int:batch>')
def delete(batch):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM spirits WHERE batch=?', (batch,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/calculators.html')
def calculators():
    return render_template('calculators.html', website_title=config_data['website_title'], website_name=config_data['website_name'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
