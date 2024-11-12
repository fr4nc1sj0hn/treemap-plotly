import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from dotenv import load_dotenv
import json
from collections import defaultdict

app = Flask(__name__)


load_dotenv()

@app.route('/api/expense-summary', methods=['GET'])
def expense_summary():
    with open('expense-summary.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/api/expense-history', methods=['GET'])
def expense_history():
    breakdown = request.args.get('breakdown')
    mode = request.args.get('mode')

    # Load data from expense-history.json
    with open('expense-history.json') as f:
        data = json.load(f)

    if mode == "category":
        filtered_data = [entry for entry in data if entry['Category'] == breakdown]
        
        monthly_totals = defaultdict(float)
        for entry in filtered_data:
            month = entry['BudgetMonth']
            monthly_totals[month] += entry['TotalExpenses']

        # Convert to a list of dictionaries for JSON response
        result = [{"BudgetMonth": month, "TotalExpenses": total} for month, total in monthly_totals.items()]
    elif mode == "subcategory":
        result = [entry for entry in data if entry['SubCategory'] == breakdown]
    else:
        monthly_totals = defaultdict(float)
        alldata = [entry for entry in data]
        for entry in alldata:
            month = entry['BudgetMonth']
            monthly_totals[month] += entry['TotalExpenses']

        result = [{"BudgetMonth": month, "TotalExpenses": total} for month, total in monthly_totals.items()]

    return jsonify(result)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/chart')
def chart():
   print('Request for chart page received')
   return render_template('chart.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
