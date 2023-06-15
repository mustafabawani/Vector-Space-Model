from ast import Dict
from cmath import log10
import math
import os
from pickle import FALSE, TRUE
import nltk
import string
from nltk.stem import PorterStemmer
import json
import tkinter as tk
from nltk import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
remove_punctuation_translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

word_stemmer = PorterStemmer()
#n= number of docs
N=448

def stopWord():
    global N
    stop_words=[]
    f=open("Stopword-List.txt")
    #make an array of all stop words
    for word in f.read().split("\n")[0:]:
        if word:
            stop_words.append(word.strip())
    return stop_words
def readFromFileAndMakeIndexes():
    i=0
    index={}
    df={}

    stop_words=stopWord()
    for k in range(0,448):
        i=i+1
        doc_id=k+1
        f=open("Abstracts\\"+str(doc_id)+".txt")
        words=[]
        new_words=[]
        #split is a built in function used to break the documents into sentences
        for line in f.read().split("\n")[0:]:
                if line:
                    #remove any punctuation in a line
                    line=line.translate(remove_punctuation_translator)
                    #nltk libarary function used to make sentences into word tokens
                    words=nltk.word_tokenize(line)
                    for items in words:
                        if len(items)>1:
                            items=items.translate(remove_punctuation_translator)
                            new_words.append(word_stemmer.stem(items))

        #Creating TermFrequency VECTOR (TF)
        temp=[]
        for word in new_words:
            if word not in stop_words:
                if word not in index:
                    index[word]=[0]*N
                index[word][k]+=1
                #Creating DocumentFrequency vector DF
                if word not in temp:
                    if df.__contains__(word):
                        df[word]+=1
                    else:
                        df[word]=1
                    temp.append(word)
        if(i==N):
            index,df=tfIdfScore(index,df)
            return index,df


#normalize index by tf=1+log(wordi) and idf=log(N/df)
#index=tf*idf
def tfIdfScore(index,df):
    global N
    for word in index:
        df[word]=math.log10(N/df[word])
        for i in range(0,N):
            index[word][i]=(1+math.log10(index[word][i]) if index[word][i]>0 else 0)
            index[word][i]=index[word][i]*df[word]
    return index,df

#process query received
def queryProcess(q,index,df):
    queryVector={}
    global N

    for word in index:
        queryVector[word]=0

    stop_words=stopWord()
    q=q.lower().split(" ")
    query_words=[]
    for q_word in q:
        if q_word not in stop_words:
            q_word=q_word.translate(remove_punctuation_translator)
            query_words.append(word_stemmer.stem(q_word))

    #Making query vector
    for q_word in query_words:
        if q_word not in stop_words:
            if q_word in index:
                queryVector[q_word]+=1
            else:
                continue
        
    #normalize query vector
    for q_word in query_words:
        if q_word in index:
            queryVector[q_word]=(1+math.log10(queryVector[q_word]) if queryVector[q_word]>0 else 0)
    for q_word in query_words:
        if q_word in index:
            queryVector[q_word]=queryVector[q_word]*df[q_word]

    docScore=similarity(index,queryVector)
    return docScore.keys()


def vectorDotProduct(v1,v2):
    dp=0
    for i in range(0,len(v1)):
            dp=dp+(v1[i]*v2[i])
    return(dp)


def vectorMagnitude(v):
    m=0
    for i in range(0,len(v)):
            m=m+(v[i]**2)
    return(math.sqrt(m))

#calculating consine similarity btw document and query vector
def cosineScore(v1,v2):
    cs=vectorDotProduct(v1,v2)
    cs=cs/(vectorMagnitude(v1))
    cs=cs/(vectorMagnitude(v2))
    return cs

def similarity(index,queryVector):
    docScore={}
    for i in range(N):
        v1=[]
        v2=[]
        #making document vector from index
        for w in index:
            v1.append(index[w][i])
            v2.append(queryVector[w])
        cs=(cosineScore(v1,v2))
        #considering alpha =0.01
        if(cs>=0.01):
            docScore[i+1]=cs
    r=dict(sorted(docScore.items(),key=lambda x:x[1]))
    r=dict(reversed(list(r.items())))
    print(r.keys())
    return docScore


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background='#00AFF0')
        self.geometry('500x500')
        self.title('Giga Search Engine')
        self.innerFrame = tk.Frame(self, height=300, width=400,background="#00AFF0")
        self.innerFrame.pack(pady=80)
        self.innerFrame.pack_propagate(0)
        self.inputLabel = tk.Label(self.innerFrame, text="Welcome to GIGA Search Engine",background="#00AFF0",font=("Bahnschrift light", 20))
        self.inputLabel.pack(pady=20)
        self.inputtxt = tk.Text(self.innerFrame,
                   height = 1,
                   width = 30)
        self.inputtxt.pack()
        self.searchButton = tk.Button(self.innerFrame,
                        text = "Search", 
                        command = self.search)
        self.searchButton.pack(pady=20)
        
        self.resultFrame = tk.Frame(self.innerFrame, height=170, width=400)
        self.resultFrame.pack()
        self.resultFrame.pack_propagate(0)
        self.unrankedResultText = tk.StringVar()
        self.resultBox = tk.Label(self.resultFrame, height=170, width=300, textvariable=self.unrankedResultText, wraplength=300,background="#00AFF0")
        self.resultBox.pack(pady=0)

        
        #make index one time in all program
        self.index,self.df=readFromFileAndMakeIndexes()
    def search(self):
        query = self.inputtxt.get(1.0, "end-1c")
        docScore=queryProcess(query,self.index,self.df)
        if "No" not in docScore:
            self.unrankedResultText.set(", ".join([str(x) for x in docScore]))
            
        else:
            self.unrankedResultText.set(docScore)


if __name__ == "__main__":
    app = Application()
    app.mainloop()