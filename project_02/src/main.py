from parse import *
from query import QueryProcessor
import operator


def main():
    qp = QueryParser('../text/queries.txt')
    cp = CorpusParser('../text/ptwiki-v2.trec.xml', '../text/stopwords.txt')
    queries = qp.queries
    corpus = cp.corpus
    proc = QueryProcessor(queries, corpus)
    results = proc.run()
    qid = 0
    for result in results:
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        print("Query: {}".format(' '.join(queries[qid])))
        for i in sorted_x[:10]:
            doc_num = i[0]
            doc_bm25_score = i[1]
            tmp = (index, doc_num, doc_bm25_score)
            print ('{:>4}\t{:>2}\t{:>12}'.format(*tmp))
            index += 1
        qid += 1


if __name__ == '__main__':
    main()
