from flask import Flask, request, render_template, redirect, make_response
import requests
import pandas as pd
import sqlite3
import getpass

# a serrver just communitcate with a client it does not or is not intended to store 
#REST api no client saving 
#the problem with tweets.txt is that it's limiited because if I want to know who wrote that tweet it won;t let you test that 


app = Flask(__name__)
conn = sqlite3.connect('twitter.db') #our database is twitter.db 

c = conn.cursor()

# Create table at the top of the table globally


#this was added so you don't need to create one every single time it runs 
#c.execute("CREATE TABLE IF NOT EXISTS twittertable (id INTEGER PRIMARY KEY AUTOINCREMENT, tweet text)") #creating a table with id and tweet - our id is an integer and we want it to be our primary key and we want to type in 
c.execute("CREATE TABLE IF NOT EXISTS twittertable (id INTEGER PRIMARY KEY AUTOINCREMENT, tweet text, user_tweet text, FOREIGN KEY(user_tweet) REFERENCES user(id))")
c.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text, registration text)")



# Insert a row of data
def insert(tweet, user, c): #the ,c is calling the c from above so we don't need to keep typing it in all the time
    # conn = sqlite3.connect('twitter.db')
    # c = conn.cursor()
    query = "INSERT INTO twittertable(tweet, user_tweet) VALUES ('{}', '{}')".format(tweet, user) #the '{}' will format all the new tweets into the tweet section if we were to just type in tweet as the value then that is what it will print  
    print(query) #looking at what it will print out 
    c.execute(query)
    # conn.commit()
    # conn.close()

def user(username, password, c):
    query = "insert into user(username, password) values ('{}','{}')".format(username, password)
    c.execute(query)


#this "/" homepage is actually the page where the user types in their tweets 
@app.route('/', methods = ['GET','POST']) 
def insert_table(): #this is creating a funtion "def name():"
    conn = sqlite3.connect('twitter.db')

    c = conn.cursor()
    curr_user = request.cookies.get('userID')
# user_id = c.execute("SELECT id FROM user WHERE username = '{}'".format(curr_user))    
    if curr_user is None:
        go_to_login = redirect('/twitter_login')
        return go_to_login

    user_tweets = c.execute("SELECT tweet FROM twittertable WHERE user_tweet= '{}'".format(curr_user))
    #it it's a POST Input: a tweet    Output: 
    if request.method == 'POST': #the client writes into the text then we receive a post from a form 
        curr_user = request.cookies.get('userID')
        tweet = request.form['text'] #getting the tweet through the form 
        insert(tweet, curr_user, c)
        conn.commit()
        user_tweets = c.execute("SELECT tweet FROM twittertable WHERE user_tweet= '{}'".format(curr_user))
        # user_tweets = c.fetchall()[0]


        print(curr_user)
        print(user_tweets)
        return render_template('twitterclone.html', get_comments=user_tweets)

        conn.close()
    else:
        return render_template('twitterclone.html', get_comments=user_tweets) 

        # curr_user_info = getpass.getuser()
    # get_comments = select_table(c) #you are calling the function from below so it will show all the tweets that were typed ie you are getting the tweets 
    
    
    
def select_table(c): #calling in the c from above 
    #input: none
    #output: tweets 
    table = c.execute("select * from twittertable;") #writing an sql statement showing all the attributes in the table 
    return table.fetchall() #this is returning all the attributes in the table


@app.route('/twitter_register', methods = ['GET','POST'])  
def register(): #this is creating a funtion "def name():"
    conn = sqlite3.connect('twitter.db')

    c = conn.cursor()

    if request.method == 'POST': #the client writes into the text then we receive a post from a form 
        username = request.form['username'] #getting the tweet through the form 
        password = request.form['password']
        user(username, password, c)
        conn.commit()
        conn.close()
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', username)


        return resp

    return render_template('register.html')

def register_table(c): #calling in the c from above 
    #input: none
    #output: registration information  
    r_table = c.execute("select registration from user;") #writing an sql statement showing all the attributes in the table 
    return r_table.fetchall() #this is returning all the attributes in the table


@app.route('/twitter_login', methods = ['GET','POST']) 
def login():
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

    if request.method == 'POST': #the client writes into the text then we receive a post from a form 
        username = request.form['username'] #getting the tweet through the form 
        password = request.form['password'] #getting the tweet through the form 
        login_user = user(username,password,c)
        conn.commit()
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', username)

        return resp

    # get_login = login_table(c) #you are calling the function from below so it will show all the tweets that were typed ie you are getting the tweets 
    return render_template('login.html') #, get_login=get_login) 

def login_table(c): #calling in the c from above 
    #input: none
    #output: login information  
    l_table = c.execute("select username, password from user;") #writing an sql statement showing all the attributes in the table 
    return l_table.fetchall() #this is returning all the attributes in the table

@app.route('/twitter_logout')
def logout():
    # username.pop('logged_in', None)
    # flash('You were logged out')
    resp = make_response(redirect('/twitter_login')) #redirects to the login page when you log out 
    resp.set_cookie('userID', '', expires=0)
    return resp

if __name__ == '__main__':
  app.run() 




#tweets
#id INT PRIMARY KEY AUTOINK
#tweet - text 
#user_id INT FOREIGN KEY 

#user table 
#id 
#username
#password  

