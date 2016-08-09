from search import Search
from invertedIndex import InvertedIndex
import json

if __name__ == "__main__":
    index = InvertedIndex("../data/ptwiki-v2.trec.xml", "../data/stopwords.txt")

    # Export index as a compressed file
    index.export_as_json("index", compressed=True)

    # Create search queries
    search_estados = Search("Estado", index)
    search_unidos = Search("Unidos", index)

    search_nomes = Search("nomes", index)
    search_biblicos = Search("bíblicos", index)

    search_winston = Search("Winston", index)
    search_churchill = Search("Churchill", index)

    # biblicos AND nomes
    nomes_and_biblicos = search_biblicos & search_nomes
    # biblicos OR nomes
    nomes_or_biblicos = search_biblicos | search_nomes

    print("nomes AND bíblicos ->{}\n\nnomes OR bíblicos->{}".format(nomes_and_biblicos, nomes_or_biblicos))

    # estados AND unidos
    estados_and_unidos = search_estados & search_unidos
    # estados OR unidos
    estados_or_unidos = search_estados | search_unidos

    print("Estados AND Unidos -> {}\n\nEstados OR Unidos -> {}".format(estados_and_unidos, estados_or_unidos))

    # winston AND churchill
    winston_and_churchill = search_winston & search_churchill
    # winston OR churchill
    winston_or_churchill = search_winston | search_churchill

    print("Winston AND Churchill -> {}\n\nWinston OR Churchill -> {}".format(winston_and_churchill, winston_or_churchill))
