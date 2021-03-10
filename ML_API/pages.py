from flask import Blueprint, render_template, url_for, redirect, request
from .__init__ import db, Info
import requests

pages = Blueprint('pages', __name__)


@pages.route('/')
def principal():
    return render_template('principal.html')


@pages.route('/', methods = ['GET', 'POST'])
def principal_input():
    # saving values from the formulary in variables
    user_name = request.form.get('user_name')
    user_age = request.form.get('user_age')
    user_fare = request.form.get('user_fare')
    user_sex = request.form.get('user_sex')
    user_pclass = request.form.get('user_pclass')
    user_parch = request.form.get('user_parch')
    user_sibsp = request.form.get('user_sibsp')

    # dict for formulary variables and API keys
    user_data = {'Age': user_age, 'Pclass': user_pclass,
                 'Sex': user_sex, 'Fare': user_fare,
                 'Parch': user_parch, 'SibSp': user_sibsp}

    # making API requests
    api_response = requests.get('http://127.0.0.1:5000/API/', user_data)
    json_response = api_response.json()
    text = json_response['Prediction']
    prob = json_response['Probability of survive']

    # saving API data in table
    user = Info(name = user_name, text = text, prob=prob)
    db.session.add(user)
    db.session.commit()

    if prob >= 50:
        return redirect(url_for('pages.alive'))

    return redirect(url_for('pages.dead'))


@pages.route('/dead')
def dead():
    # this query takes the last input in the table
    user = Info.query.order_by(Info.id.desc()).first()
    return render_template('dead.html', user= user)

@pages.route('/alive')
def alive():
    user = Info.query.order_by(Info.id.desc()).first()
    return render_template('alive.html', user=user)
