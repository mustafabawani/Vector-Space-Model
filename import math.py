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
def stopWord():
    stop_words=[]
    f=open("Stopword-List.txt")
    #make an array of all stop words
    for word in f.read().split("\n")[0:]:
        if word:
            stop_words.append(word.strip())
    return stop_words
def readFromFileAndMakeIndexes():
    i=0
    vectorSpace=[]
    docVector=[]
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
                            items=lemmatizer.lemmatize(items)
                            new_words.append(items.lower())

        #Creating TermFrequency VECTOR (TF)
        tf={}
        temp=[]
        for word in new_words:
            if tf.__contains__(word):
                tf[word]+=1
            else:
                if word not in vectorSpace:
                    vectorSpace.append(word)
                tf[word]=1
            if word not in temp:
                if df.__contains__(word):
                    df[word]+=1
                else:
                    df[word]=1
                temp.append(word)
        docVector.append(tf)
        if(i==50):

            docVector,df=tfIdfScore(vectorSpace,docVector,df)
            return vectorSpace,docVector,df
def tfIdfScore(vectorSpace,docVector,df):
    N=len(docVector)
    # print(N)
    # print(df)
    # print(docVector)
    # vectorSpace=set(vectorSpace)
    for word in vectorSpace:
        for d in docVector:
            if d.__contains__(word):
                # print(d[word])
                d[word]=1+math.log10(d[word])
            else:
                d[word]=0
        df[word]=math.log10(N/df[word])
    # print(df)
    # print(docVector)
    for word in df:
        for d in docVector:
            d[word]=d[word]*df[word]
    # print(df)
    # print(docVector)
    return docVector,df

def queryProcess(q,vectorSpace,df):
    queryVector={}
    N=2
    for word in vectorSpace:
        queryVector[word]=0
    stop_words=stopWord()
    q=q.lower().split(" ")
    for q_word in q:
        if q_word not in stop_words:
            if q_word in vectorSpace:
                queryVector[q_word]+=1
            else:
                continue
    for q_word in q:
        queryVector[q_word]=1+math.log10(queryVector[q_word])
    for q_word in q:
        queryVector[q_word]=queryVector[q_word]*df[q_word]
    similarity(docVector,queryVector)
    # print(queryVector)
    # print(q)

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

def cosineScore(v1,v2):
    cs=vectorDotProduct(v1,v2)
    cs=cs/(vectorMagnitude(v1)*vectorMagnitude(v2))
    return cs
def similarity(docVector,queryVector):
    v1=[]
    v2=[]
    docScore=[]
    # print(queryVector)
    for i in range( len(docVector)):
        for word in queryVector:
                v1.append(docVector[i][word])
                v2.append(queryVector[word])
        docScore.append(cosineScore(v1,v2))
    print(docScore)
vectorSpace,docVector,df=readFromFileAndMakeIndexes()
queryProcess("markov",vectorSpace,df)
