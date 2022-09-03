import os
from pickle import FALSE, TRUE
import re
import nltk
from nltk.stem import PorterStemmer
path = r"C:\Users\Shahriyaar\OneDrive\Desktop\IR assignment\Abstracts"
a=[]
def position_query(query,position_index):
    #query= input("enter query  :  " )
    word_apart=query[len(query)-1]  #number of positions terms can be displaced
    query=query[:-3] #deleting /k from query
    query=re.sub(r'[^\w\s]','',query) #deleting punctuations
    query=nltk.word_tokenize(query)  #tokenizing terms
    query=[stemmer.stem(i) for i in query] #stemming
    for i in range(len(query)-1):
        if(query[i] not in position_index or query[i+1] not in position_index):
            print('one term not found')
            return
        term1=position_index.get(query[i])  
        term2=position_index.get(query[i+1])
        intersect=set(term1).intersection(term2)   #taking intersection
    #print(intersect)
    answer=[]
    # print(intersect)
    print('\n\n\n')
    for i in intersect:
        # print(position_index.get(query[0]))
        p1 = position_index.get(query[0])[i]
        p2 = position_index.get(query[1])[i]
        len1 = len(p1)
        len2 = len(p2)
        i1 = j1 = 0 
        while i1 != len1:
            while j1 != len2:
                if (abs(p1[i1]-p2[j1])<=int(word_apart)+1):
                    answer.append(i)
                elif p2[j1] > p1[i1]:
                    break 
                j1+=1
            i1+=1
    answer = list(dict.fromkeys(answer))
    print(answer)

def not_function(query,inverted_index):
    query.remove('not')
    universal=[i for i in range(1,449)]
    if query[0] not in inverted_index:
        print(universal)
        return
    inv=inverted_index[query[0]]
    res_query=set(universal).difference(set(inv))
    print(res_query)

def boolean_query(query,inverted_index):
    #print(a[186])
    #query=input("enter the query")
    stemmer=PorterStemmer()
    query=query.lower()
    query=nltk.word_tokenize(query)
    res_query=[]
    ans=[]
    flag=1
    if 'not' in query:
        not_function(query,inverted_index)
        return
    if 'or' in query:
        or_word=query[query.index('or')+1]
        query.remove(or_word)
        ans=ans+inverted_index[stemmer.stem(or_word)]
    for i in query:
        if i not in ['and','or']:
            res_query.append(i)
    res_query=[stemmer.stem(i) for i in res_query]
    #print(res_query)
    res_list=[]
    count=0
    for i in res_query:
        if i not in inverted_index:
            print(i+"  term not found")
            return
    for i in res_query:
        res_list.append(inverted_index[i])
        count=count+1
    #print(res_list[0])
    for i in res_list[0]:
        #print('this is'+str(i))
        flag=TRUE
        for j in range(1,count):
            #print(res_list[j])
            if(i not in res_list[j]):
                flag=FALSE
                break
        if(flag == TRUE):
            ans.append(i)
    
    #print(inverted_index[stemmer.stem(or_word)])
    ans=list(set(ans))  #deletes duplicate items
    ans=sorted(ans)
    print(ans)




def read_text_file(file_path,file):
    #reading stopword list and separating each word
    f=open(r'C:\Users\Shahriyaar\OneDrive\Desktop\IR assignment\Stopword-List.txt')
    s=f.read()
    s=nltk.word_tokenize(s)
    os.chdir(path)
    with open(file_path, 'r') as f:
        c=f.read()   #reading file
        c=c.lower()
        for i in ['-',',','/']:
            c=c.replace(i,' ')
        c=re.sub(r'[^\w\s]','',c)  #deleting punctuations 
        #c=re.sub("\-([a-zA-Z]+)", r"\1", c)
        c=nltk.word_tokenize(c)  #tokinizing words
        c_without_stop = [i for i in c if not i in s]  #removing stopwords
        stemmer=PorterStemmer() 
        c_stemmer=[stemmer.stem(i) for i in c_without_stop]
        a.insert(int(file[:len(file)-4]),c_stemmer)  #creating a list where each index contains tokens of the i+1th index



for i in range(1,449):
    file=str(i)+'.txt'
    file_path = f"{path}\{file}"
    read_text_file(file_path,file)
    
#print(a[444])
inverted_index={}
for i in a:
    for j in i:
        if j not in inverted_index:
            inverted_index[j]=[]
        if j in inverted_index:
            inverted_index[j].append(a.index(i)+1)
#print(inverted_index)
stemmer=PorterStemmer()
""" print(stemmer.stem('produce'))
if stemmer.stem('produce') in inverted_index:
    print(inverted_index[stemmer.stem('produce')]) """
position_index={}
for i in a:
    counter=0
    for pos, term in enumerate(i):
        if term not in position_index:
            position_index[term]={}
            position_index[term][a.index(i)+1]=[]
        if(term in position_index):
            if(a.index(i)+1 in position_index[term]):
                position_index[term][a.index(i)+1].append(counter)   
                
            else:
                position_index[term][a.index(i)+1]=[]
                position_index[term][a.index(i)+1].append(counter)
        counter=counter+1
print("                    welcome to boolean retrieval model                      ")
query=input("                    enter your desired query: ")
if('/' in query):
    position_query(query,position_index)
else:
    boolean_query(query,inverted_index)