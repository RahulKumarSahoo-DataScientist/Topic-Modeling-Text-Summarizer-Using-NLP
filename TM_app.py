#importing flask
from flask import Flask, render_template,request
import json
import gensim
import string
from gensim import corpora
from nltk.corpus import stopwords
import pandas as pd 
from flaskext.markdown import Markdown
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
app = Flask(__name__)# If you want to know which URL should be used to call the associated method, use the route() function of Flask's class. The URL binding with the function is represented by the rule's rule argument.
Markdown(app)
@app.route("/")#In this case, mapping the URLs to a function that will handle the logic for each individual URL
def msg():
    # Giving a result
    return render_template('index.html')
    
@app.route("/topics",methods=['POST','GET'])# If the gateway is unable to obtain the client's IP address, this information will be missing from the request.
def gettopics():
    text=request.form['data']# Sending a request
    text_without_punct = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize the text
    text_list = gensim.utils.simple_preprocess(text_without_punct)

    # Remove stopwords
    stop_words = stopwords.words("english")
    text_list = [word for word in text_list if word not in stop_words]

    # Create the Dictionary and Corpus
    dictionary = corpora.Dictionary([text_list])
    corpus = [dictionary.doc2bow(text_list)]

    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    #ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    result=[]
    for topic in topics:
      result.append(topic)
    df = pd.DataFrame (result, columns = ['Topic Number', 'Topic'])
    df=df.iloc[:,1:]
    docx=nlp(text)
    html=displacy.render(docx,style="dep")
    html=html.replace("\n\n","\n")
    result=HTML_WRAPPER.format(html)
    html1=displacy.render(docx,style='ent')
    result1=HTML_WRAPPER.format(html1)
   
      # Defining instances
    return render_template('topic.html',result1=result1,result=result,tm=df.to_html())
    
if __name__ =="__main__":# When modules are imported, it allows or deny certain code to be executed.
    app.run(debug=True,port=8000)#IP address on which a Web client can communicate with the server.