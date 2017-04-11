#A quick look at exracting academic networks from archive.org
from internetarchive import *
import networkx as nx
import logging


logging.basicConfig(filename = 'log.txt', level=logging.DEBUG)

def search_creator(creator):
    out = []
    for i in search_items('creator:{}'.format(creator)):
        out.append(i)
    return out

def get_authors_of_paper(paper_id):
    item = get_item(paper_id).item_metadata
    if 'metadata' in item.keys():
        creators = item['metadata']['creator']
        print(creators)
    else:
        logging.warning('No metadata for {}'.format(paper_id))
        creators = []
    return creators

def flatten(array):
    return [i for out2 in array for i in out2]

def searching_seed(seed):
    out = []
    temp = search_creator(seed)
    for element in temp:
        out.append(get_authors_of_paper(element['identifier']))
    return out

def process_authors(to_be_done):
    new_authors = set()
    for author in to_be_done:
        print(author)
        co_authors=searching_seed(author)
        for co_author in co_authors:
            if type(co_author) == str:
                G.add_edge(author,co_author)
                new_authors.add(co_author)
            if type(co_author) == list:
                for individual_co_author in co_author:
                    G.add_edge(author,individual_co_author)
                    new_authors.add(individual_co_author)
        done.add(author)
    return new_authors




if __name__ == '__main__':

    G = nx.Graph()
    
    G.add_node('Meagher')
    
    to_be_done = set()
    done = set()
    to_be_done.add('Meagher')
    
    #temp = search_creator(G.nodes[0])
    #out = []
    #for element in temp:
    #    out.append(get_authors_of_paper(element['identifier']))
    #
    #out = set(flatten(out))
    
    #for i in range(0,100):
    
    i=0
    while i < 10:
        print(i)
        new_authors = process_authors(to_be_done)
        for new_author in new_authors:
            to_be_done.add(new_author)
        to_be_done.difference_update(done)
        nx.write_gml(G,'output_' + str(i) + '.gml')
        i = i+1
    
    nx.write_gml(G,'output.gml')

#    to_be_done.difference_update(done)
#
#    for author in to_be_done:
#        co_authors=searching_seed(author)
#
#        for co_author in co_authors:
#            if type(co_author) == str:
#                G.add_edge(author,co_author)
#                to_be_done.add(co_author)
#            if type(co_author) == list:
#                for individual_co_author in co_author:
#                    G.add_edge(author,individual_co_author)
#                    to_be_done.add(individual_co_author)
#        done.add(author)

#    i = i + 1

