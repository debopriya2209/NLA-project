from flask import Flask, render_template, request,Response,redirect,jsonify
from flask_bcrypt import Bcrypt

import db_connect
import cursor_module

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signUp')
def sign_up():
    return render_template('register.html')
    

@app.route('/logIn', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        user_name=request.form['username']
        password=request.form['password']
        print(user_name,password)
        result=db_connect.Sign_In(user_name)
        print('result',result)
        if result == None:
            message='UserName Does Not Exists'
            return render_template('login.html',message=message)
        #if result['password'] == password:
        if (bcrypt.check_password_hash(result['password'],password)):
            return redirect('/home')
        else:
            message='Enter A Valid Password'
            return render_template('login.html',message=message)
        
        print('result',result)

@app.route('/enroll',methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        name=request.form['name']
        user_name=request.form['username']
        password=request.form['password']
        pw_hash = bcrypt.generate_password_hash(password)
        print('hash->',pw_hash)
        print("-->",name,user_name,password)
        count=db_connect.Register(name,user_name,pw_hash)
        print("Controller Count->",count)
        if count == 1:
            return redirect('/')
        message="UserName Already Exists"
        return render_template('register.html', message=message)

@app.route('/home')
def home():

    return render_template('home.html')
    
@app.route('/search',methods=['POST'])
def search():
    word=request.form['word']
    top_five,search.percent_pos_tweets,search.percent_neu_tweets,search.percent_neg_tweets \
    ,top_three_pos_tweets,top_three_neu_tweets,top_three_neg_tweets=cursor_module.sentiment_percentage(word)
    print("keyword",word)
    #print("top_five",top_five)
    return render_template('searchResult.html',tweets=top_five.tolist \
    (),tweets_pos=top_three_pos_tweets,tweets_neg=top_three_neg_tweets,tweets_neu=top_three_neu_tweets)

@app.route('/chart',methods=['POST'])
def chart():
    pos=search.percent_pos_tweets
    neg=search.percent_neg_tweets
    neu=search.percent_neu_tweets
    data={'positive':pos,'negative':neg,'neutral':neu}
    print(pos)
    return jsonify(data)
    #return render_template('pie.html')



if __name__ == "__main__":
    app.secret_key="abc"
    app.debug=False
    app.run()
