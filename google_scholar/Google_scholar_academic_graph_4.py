
import zs.bibtex as zs
from zs.bibtex.parser import parse_string
import networkx as nx
import itertools
import subprocess



def parsing_csv(data):
    temp = str(data)[2:].split('@')
    temp = ['@' + i.replace('\\n','').replace("'","").replace('"','') for i in temp]
    temp = [parse_string(i) for i in temp[1:]]
    return temp



def processing_parse(data):
    out = [i[list(i.keys())[0]]['author'] for i in data]
    return out



def processing_parse(data):
    out = []
    for i in data:
        authors = i[list(i.keys())[0]]['author']
        title = i[list(i.keys())[0]]['title']
        out.append({'author':authors,'title':title})
        print(authors,title)
    return out
        #print(i[list(i.keys())[0]]['author'])



def python_request_author(author):
    test = subprocess.Popen(["python2", "scholar.py","-c","50","-a","{}".format(author),'--citation=bt'], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    return output

def python_request_words(words):
    test = subprocess.Popen(["python2", "scholar.py","-c","50","-all","{}".format(words),'--citation=bt'], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    return output


G = nx.Graph()
author_list = []
seed_word = 'Graphene'
initial_seed = python_request_words(seed_word)
initial_seed_processed = parsing_csv(initial_seed)
for paper in initial_seed_processed:
    #paper[list(paper.keys())][0]
    element = paper[list(paper.keys())[0]]
    authors = element['author']
    title = element['title']
    for author in authors:
        author_list.extend([author])
        G.add_node(author,title = title)
    a = list(itertools.combinations(authors,2))
    for i in a:
        G.add_edge(*i)

for author in author_list:
    print(author)
    temp = python_request_author(author)
    if len(temp) == 0:
        print('Request limit reached')
        break 
    temp = parsing_csv(temp)
    temp = processing_parse(temp)
    for element in temp:
        for author_2 in element['author']:
            author_list.append(author_2)
            G.add_node(author,title = element['title'])
        
        a = list(itertools.combinations(element['author'],2))
        for i in a:
            G.add_edge(*i)
    nx.write_gml(G,seed_word + '.gml')
    nx.write_gpickle(G,seed_word + '.pickle')
            
print('Hello')
