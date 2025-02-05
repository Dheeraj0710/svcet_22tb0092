
from form import NameForm
from flask import Flask, render_template
app=Flask(__name__)
app.config['SECRET_KEY']='1234'
@app.route('/forms',methods={'GET','POST'})

def form():
    form =NameForm()
    if form.validate_on_submit():
        return f"hello,{form.name.data}!"
    return render_template('form.html',form=form)


if __name__=='__main__':
  app.run(debug=True)