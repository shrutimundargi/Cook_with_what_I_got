from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        ingredients = request.form.get('fname')
        data = pd.read_csv("indian_food.csv")
        data = data.drop(columns=['flavor_profile','region','state', 'diet'])
        str_cols = list(data.columns)
        str_cols.remove('prep_time')
        str_cols.remove('cook_time')
        for i in str_cols:
            data[i] = data[i].str.strip()
            data[i] = data[i].str.lower()
        for i in ['name']:
          data[i] = data[i].str.replace(" ", "-")
        for i in ['course']:
          data[i] = data[i].str.replace(" ", "-")
        for i in ['ingredients']:
          data[i] = data[i].str.replace(" ", "-")
          data[i] = data[i].str.replace(",-", "_")
          data[i] = data[i].str.replace("_", ", ")
        data['ingredients'] = list(data['ingredients'])
        available = []
        suggested = []
        recommendation = pd.DataFrame(columns = ['recipe', 'ingredients', 'score'])
        for i in range(0, len(data)):
            count = 0
            for j in ingredients:
                if j in data['ingredients'][i]:
                    count +=1
                    available.append(j)
            if count >= 3:
                series = pd.DataFrame({'recipe': [data['name'][i]], 'ingredients': data['ingredients'][i], 'score': "{:.2f}".format((len(available))/(len(data['ingredients'][i]))*100)})
                recommendation = recommendation.append(series)
                available.clear()
                
        return render_template("dishrec.html", tables=[recommendation.to_html(classes='data')],titles = ['Recommendations'])

    else: 
        return render_template("dishrec.html",res="")

if __name__ == '__main__':
    app.run(debug = True)