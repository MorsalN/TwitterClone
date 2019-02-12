from flask import Flask, request, render_template
import requests
import pandas as pd
import sqlite3

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
c.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)")



# Insert a row of data


def insert(tweet, c): #the ,c is calling the c from above so we don't need to keep typing it in all the time
    query = "INSERT INTO twittertable(tweet) VALUES ('{}')".format(tweet) #the '{}' will format all the new tweets into the tweet section if we were to just type in tweet as the value then that is what it will print  
    print(query) #looking at what it will print out 
    c.execute(query)

@app.route('/twitter_clone', methods = ['GET','POST']) 
def insert_table(): #this is creating a funtion "def name():"
    conn = sqlite3.connect('twitter.db')

    c = conn.cursor()

    #it it's a POST Input: a tweet    Output: 
    if request.method == 'POST': #the client writes into the text then we receive a post from a form 
        tweet = request.form['text'] #getting the tweet through the form 
        insert(tweet, c)
        conn.commit()
    get_comments = select_table(c) #you are calling the function from below so it will show all the tweets that were typed ie you are getting the tweets 
    return render_template('twitterclone.html', get_comments=get_comments) 
    
    
def select_table(c): #calling in the c from above 
    #input: none
    #output: tweets 
    table = c.execute("select * from twittertable;") #writing an sql statement showing all the attributes in the table 
    return table.fetchall() #this is returning all the attributes in the table


#tweets
#id INT PRIMARY KEY AUTOINK
#tweet - text 
#user_id INT FOREIGN KEY 

#user table 
#id 
#username
#password  

