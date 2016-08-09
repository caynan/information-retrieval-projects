import json
import gzip
import shutil

from collections import defaultdict

# TODO: implement abstract class for index type (must implement search
# method that return a searchResult object)


class InvertedIndex:
    """An Inverted index, it can be created using a wikipedia dump

    Attributes:
        index: dict
             Inverted index created from the given dump_filepath
    """

    def __init__(self, corpus):
        """ Tokenize an wikipedia XML Dump

        Parameters
        ----------
        dump_filepath: str
              filepath for the xml dump to be processed
        stopword_filepath: str
              filepath for stopwords (file must contain one  stopword per line)
        """
        self._index = self._create_index(corpus)

    def __contains__(self, token):
        return token in self._index

    def __getitem__(self, token):
        return self._index[token]


    @property
    def index(self):
        """Get the inverted index
        Returns
        -------
        dict
             A dictionary on the format {'doc_num': [token_0, token_1, ..., token_n], ...}
        """
        return self._index

    def search(self, search_term):
        """search in our index
        Returns
        -------
        set
             A set on the format {doc1, doc2, doc3, ... , docn}
        """
        return self.index[search_term.lower()]

    def export_as_json(self, filename="index", compressed=False):
        """ Export index to a file, (optional: give name for file,
            choose if file should be compressed)

        Parameters
        ----------
        filename: str (optional)
              filepath of the output file
        isGzip: boolean (optional)
              if we should compress our index file
        """
        # transform index to be a dict of list not sets (since json don't
        # support sets)
        temp_index = {token: list(docs)
                                  for (token, docs) in self.index.items()}
        # add json extention to filepath
        filepath = filename + ".json"

        if compressed:
            filepath += ".gz"
            with gzip.open(filepath, mode="wt") as json_file:
                json.dump(temp_index, json_file, ensure_ascii=False,
                          sort_keys=True, indent=4)
        else:
            with open(filepath, 'w', encoding='utf8') as json_file:
                json.dump(temp_index, json_file, ensure_ascii=False,
                          sort_keys=True, indent=4)

    def _create_index(self, corpus):
        """ Create index from given corpus

        Parameters
        ----------
        index: dict
              A dictionary on the format {'doc_num': [token_0, token_1, ..., token_n], ...}

        Returns
        -------
        dict
             An inverted dictionary on the format {'token': set(doc_1, doc_2, ... , doc_n)}
             where each doc represent a document that contains the given token
        """
        index = dict()
        for doc_num, tokens in corpus.items():
            for token in tokens:
                self._add(token, doc_num, index)
        return index

    def _add(self, token, doc_num, index):
        if token in index:
            if doc_num in index[token]:
                index[token][doc_num] += 1
            else:
                index[token][doc_num] = 1
        else:
            d = dict()
            d[doc_num] = 1
            index[token] = d

    def get_document_frequency(self, word, docid):
        """ Get term frequency of token on given doc_num

        Parameters
        ----------
        token: str
              A given token to be searched
        doc_num: str
              A given doc_num to search on

        Returns
        -------
        int
            If exists, the number of occurences of token on given doc_num.
            Raises a LookupError otherwise
        """
        if word in self._index:
            if docid in self._index[word]:
                return self._index[word][docid]
            else:
                raise LookupError('%s not in document %s' % (str(word), str(docid)))
        else:
            raise LookupError('%s not in index' % str(word))


    def get_index_frequency(self, word):
        """ Get inverse document frequency of token on the whole index

        Parameters
        ----------
        token: str
              A given token to be searched

        Returns
        -------
        int
            If exists, the number of occurences of documents that contain the given token.
            Raises a LookupError otherwise.
        """
        if word in self._index:
            return len(self._index[word])
        else:
            raise LookupError('%s not in index' % word)


class DocumentLengthTable:
    """A document length table, it stores the length of individual documents,
        and the document length average of the index.
    """
    def __init__(self, corpus):
        self.table = dict()
        self._mean_document_average = 0.0
        self._indexed_documents_count = 0

        self.create_document_table(corpus)


    def __len__(self):
        return len(self.table)


    def create_document_table(self, corpus):
        for docid in corpus:
            length = len(corpus[str(docid)])
            self.add(docid, length)


    def add(self, docid, length):
        self.table[docid] = length
        self._update_average(length)


    def _update_average(self, length):
        self._indexed_documents_count += 1
        updated_average = self._mean_document_average + ((length - self._mean_document_average) / self._indexed_documents_count)

        self._mean_document_average = updated_average


    def get_length(self, docid):
        if docid in self.table:
            return self.table[docid]
        else:
            raise LookupError('%s not found in table' % str(docid))


    def get_average_length(self):
        return self._mean_document_average


def build_data_structures(corpus):
    idx = InvertedIndex(corpus)
    dlt = DocumentLengthTable(corpus)

    return idx, dlt
