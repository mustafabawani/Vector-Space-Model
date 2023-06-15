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
    #getcwd brings the existing path of file
    # path=os.getcwd()
    # path=path+'/Abstracts/'
    #getting all files in path
    # files=os.listdir(path)
    i=0
    vectorSpace=[]
    docVector=[]
    df={}
    stop_words=stopWord()
    # print(stop_words)
    # for file in files:
    for i in range(448):
        doc_id=i+1

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
                    # print(line)
                            # new_words.append(word_stemmer.stem(items))                    
        #patition function is sued to break string at the first occurence of '.'
        # doc_id=(file.partition(".")[0])
        #convert from sting to int 
        doc_id=int(doc_id)

        #Creating TermFrequency VECTOR (TF)
        tf={}
        temp=[]
        # flag=False
        for word in new_words:
            if tf.__contains__(word):
                tf[word]+=1
                # print(word)
            else:
                vectorSpace.append(word)
                tf[word]=1
            if word not in temp:
                if df.__contains__(word):
                    df[word]+=1
                else:
                    df[word]=1
                temp.append(word)
            
        docVector.append(tf)
        if(i==100):
            docVector,df=tfIdfScore(vectorSpace,docVector,df)
            print(docVector)
            return vectorSpace,docVector,df

def tfIdfScore(vectorSpace,docVector,df):
    N=len(docVector)
    for word in vectorSpace:
        for d in docVector:
            if word in d:
                # print(d[word])
                d[word]=1+math.log10(d[word] if d[word]>0 else 1)
            # else:
            #     d[word]=0
        df[word]=math.log10(N/df[word] if df[word]>0 else 1)
    # print(docVector)
    for word in df:
        for d in docVector:
            if word in d:
                d[word]=d[word]*df[word]
    return docVector,df

def queryProcess(q,vectorSpace,df,docVector):
    queryVector={}
    N=len(docVector)
    for word in vectorSpace:
        queryVector[word]=0
    stop_words=stopWord()
    q=q.lower().split(" ")
    for q_word in q:
        # lemmatizer.lemmatize(q_word)
        if q_word not in stop_words:
            if q_word in vectorSpace:
                queryVector[q_word]+=1
            else:
                continue
    for q_word in q:
        if q_word in vectorSpace:
            queryVector[q_word]=1+math.log10(queryVector[q_word])
    for q_word in q:
        if q_word in vectorSpace:
            queryVector[q_word]=queryVector[q_word]*df[q_word]
    similarity(q,docVector,queryVector)
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
    vm=vectorMagnitude(v1)*vectorMagnitude(v2)
    if vm==0:
        cs=0
    else:
        cs=cs/(vm)
    return cs
def similarity(q,docVector,queryVector):
    docScore={}
    print(queryVector)
    docCount=0
    for i in range(0,len(docVector)):
        v1=[]
        v2=[]
        for word in q:
            if word in docVector[docCount]:
                v1.append(docVector[docCount][word])
                v2.append(queryVector[word])
            # if word=="ensemble":
            #     print(docVector[docCount][word],queryVector[word])
        docCount+=1
        docScore[docCount]=(cosineScore(v1,v2))
    print(docScore)
vectorSpace,docVector,df=readFromFileAndMakeIndexes()
queryProcess("ensemble",vectorSpace,df,docVector)
