#importing flask
from flask import Flask, render_template,request
#Importing the summarizer
#from summarizer import Summarizer
#from summarizer.sbert import SBertSummarizer

# Using an instance of SBERT to create the model
#model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
import nltk
nltk.download('stopwords')

from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest

from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest

STOPWORDS = set(stopwords.words('english') + list(punctuation))
MIN_WORD_PROP, MAX_WORD_PROP = 0.1, 0.9


def compute_word_frequencies(word_sentences):
    words = [word for sentence in word_sentences 
                     for word in sentence 
                         if word not in STOPWORDS]
    counter = Counter(words)
    limit = float(max(counter.values()))
    word_frequencies = {word: freq/limit 
                                for word,freq in counter.items()}
    # Drop words if too common or too uncommon
    word_frequencies = {word: freq 
                            for word,freq in word_frequencies.items() 
                                if freq > MIN_WORD_PROP 
                                and freq < MAX_WORD_PROP}
    return word_frequencies

def sentence_score(word_sentence, word_frequencies):
    return sum([ word_frequencies.get(word,0) 
                    for word in word_sentence])

def summarize(text:str, num_sentences=3):
    """
    Summarize the text, by return the most relevant sentences
     :text the text to summarize
     :num_sentences the number of sentences to return
    """
    text = text.lower() # Make the text lowercase
    
    sentences = sent_tokenize(text) # Break text into sentences 
    
    # Break sentences into words
    word_sentences = [word_tokenize(sentence) for sentence in sentences]
    
    # Compute the word frequencies
    word_frequencies = compute_word_frequencies(word_sentences)
    
    # Calculate the scores for each of the sentences
    scores = [sentence_score(word_sentence, word_frequencies) for word_sentence in word_sentences]
    sentence_scores = list(zip(sentences, scores))
    
    # Rank the sentences
    top_sentence_scores = nlargest(num_sentences, sentence_scores, key=lambda t: t[1])
    
    # Return the top sentences
    return [t[0] for t in top_sentence_scores]





app = Flask(__name__)# If you want to know which URL should be used to call the associated method, use the route() function of Flask's class. The URL binding with the function is represented by the rule's rule argument.

@app.route("/")#In this case, mapping the URLs to a function that will handle the logic for each individual URL
def msg():
    # Giving a result
    return render_template('index.html')
    
@app.route("/summarize",methods=['POST','GET'])# If the gateway is unable to obtain the client's IP address, this information will be missing from the request.
def getSummary():
    body=request.form['data']# Sending a request
    result = summarize(body, num_sentences=5)# Defining instances
    return render_template('summary.html',result=result)
    
if __name__ =="__main__":# When modules are imported, it allows or deny certain code to be executed.
    app.run(debug=True,port=8000)#IP address on which a Web client can communicate with the server.