from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

