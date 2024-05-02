from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import math  # math モジュールを追加

app = Flask(__name__)
app.config['DATABASE'] = 'sweets2.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        num_boxes = int(request.form['num_boxes'])
        cur.execute("SELECT * FROM Recipes")
        recipes = cur.fetchall()
        modified_recipes = []
        for recipe in recipes:
            can = int(recipe['can'])
            unit = int(recipe['unit'])
            scale_factor = math.ceil((num_boxes * can) / unit)  # 製造数量と缶の数を掛け、単位で割って繰り上げる
            modified_recipe = dict(recipe)
            modified_recipe['rice_flower'] = int(recipe['rice_flower']) * scale_factor
            modified_recipe['soy_milk'] = int(recipe['soy_milk']) * scale_factor
            modified_recipe['coconut_oil'] = int(recipe['coconut_oil']) * scale_factor
            modified_recipe['brown_sugar'] = int(recipe['brown_sugar']) * scale_factor
            modified_recipe['starch'] = int(recipe['starch']) * scale_factor
            modified_recipe['almond'] = int(recipe['almond']) * scale_factor
            modified_recipe['cocoa'] = int(recipe['cocoa']) * scale_factor
            modified_recipe['raspberry'] = int(recipe['raspberry']) * scale_factor
            modified_recipe['lemon'] = int(recipe['lemon']) * scale_factor
            modified_recipe['baking_soda'] = int(recipe['baking_soda']) * scale_factor
            modified_recipes.append(modified_recipe)
        
        return render_template('can_ingredients.html', recipes=modified_recipes)

    return render_template('index.html')

@app.route('/admin/login', methods=['GET'])
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'sunabaco':
            return redirect(url_for('admin_dashboard'))
        else:
            return "パスワードが正しくありません"
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        serving_size = request.form['serving_size']
        serving_unit = request.form['serving_unit']
        cur.execute("INSERT INTO Recipes (name, serving_size, serving_unit) VALUES (?, ?, ?)", (recipe_name, serving_size, serving_unit))
        db.commit()
    cur.execute("SELECT * FROM Recipes")
    recipes = cur.fetchall()
    return render_template('admin_dashboard.html', recipes=recipes)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM Recipes WHERE id = ?", (recipe_id,))
        recipe = cur.fetchone()
        if recipe:
            return render_template('edit_recipe.html', recipe=recipe)
        else:
            return "レシピが見つかりません"
    elif request.method == 'POST':
        recipe_name = request.form['recipe_name']
        serving_size = request.form['serving_size']
        serving_unit = request.form['serving_unit']
        cur.execute("UPDATE Recipes SET name = ?, serving_size = ?, serving_unit = ? WHERE id = ?", (recipe_name, serving_size, serving_unit, recipe_id))
        db.commit()
        return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
