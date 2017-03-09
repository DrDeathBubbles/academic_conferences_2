 #small programme to
import requests
import networkx as nx
import itertools
import xmltodict
#import pandas as pd
#%pylab inline 

def search_all(term,start,stop):
    r = requests.get('http://export.arxiv.org/api/query?search_query=all:{}&start={}&max_results={}'.format(term,start,stop))
    return xmltodict.parse(r.text)

def search_author(author,start,stop):
    r = requests.get('http://export.arxiv.org/api/query?search_query=au:{}&start={}&max_results={}'.format(author,start,stop))
    return xmltodict.parse(r.text)

def authors_and_titles(b):
    temp1 = []
    temp2 = []
    temp4 = []
    temp5 = []
    
    if 'entry' not in b['feed'].keys():
        return
    
    
    if type(b['feed']['entry']) == list:
        for entry in b['feed']['entry']:
            if type(entry['author']) == list:
                temp3 = []
                for author in entry['author']:
                    temp3.append(author['name'])
                    temp4.extend([author['name']])
                temp1.append(temp3)
                temp5.append({'author':temp3,'title':entry['title']})
            else: 
                temp4.extend([entry['author']['name']])
                temp1.append(entry['author']['name'])
                temp5.append({'author':entry['author']['name'],'title':entry['title']})
            #temp1.append(entry['author'])
            #temp1.append(entry['author'])
            temp2.append(entry['title'])
        return [temp5,temp1,temp4]
    else:
        return


def new_network_generation(c):
    for element in c:
        if 'author' in element.keys():
            for author in element['author']:
                G.add_node(author,title = element['title'])

            a = list(itertools.combinations(element['author'],2))
            for i in a:
                G.add_edge(*i)
                

                
def run_network_analysis(word,length_1,length_2):                
    #Initial seed
    G = nx.Graph()
    a = search_all(word,0,length_1)

    author_list = authors_and_titles(a)

    for i in author_list[2]:
        b = search_author(i,'0',str(length_2))
        b = authors_and_titles(b)
        if type(b) != type(None):
            new_network_generation(b[0])
    return G          
                

def saving_graph(G,output_file):
    with open(output_file,'a') as f:
        for node in G.nodes():
            f.write("{},{}\n".format(node,G.node[node]['title'].replace(',','').replace('\n','')))

    
    
    
    
if __name__ == '__main__':                
    #Initial seed
    #G = nx.Graph()
    #temp = run_network_analysis('Graphene',10,10)
    #Initial seed
    seed_words = ['nano','star','dynamic','galaxy','galaxies','cosmic','the','active']    
    for seed_word in seed_words:
        G = nx.Graph()
        a = search_all(seed_word,0,100)

        author_list = authors_and_titles(a)

        for i in author_list[2]:
            b = search_author(i,'0','100')
            b = authors_and_titles(b)
            if type(b) != type(None):
                new_network_generation(b[0])
            
        saving_graph(G,seed_word+'.csv')
        nx.write_gpickle(G,seed_word+'.pickle')
    




