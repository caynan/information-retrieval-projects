import xml.etree.ElementTree as ET
import re


class CorpusParser:

    def __init__(self, dump_filepath, stopword_filepath):
        self._stopwords = set(open(stopword_filepath).read().split())
        self._corpus = self._tokenize(dump_filepath)

    @property
    def corpus(self):
        return self._corpus

    def _tokenize(self, dump_filepath):
        """ Tokenize an wikipedia XML Dump

        Parameters
        ----------
        dump_filepath: str
              filepath for the xml dump to be processed
        stopword_filepath: str
              filepath for stopwords (file must contain one  stopword per line)

        Returns
        -------
        dict
             A dictionary on the format {'doc_num': [token_0, token_1, ..., token_n], ...}
        """
        tree = ET.parse(dump_filepath)
        root = tree.getroot()

        documents = {}
        for child in root:
            doc_num = child.find('DOCNO').text
            text = child.find('P').text
            text = self._sanitize(text)

            documents[doc_num] = text.split()

        return documents

    def _create_index(self, data):
        """ Create index from given string

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
        index = defaultdict(set)
        for doc_num, tokens in data.items():
            for token in tokens:
                index[token].add(doc_num)
        return index

    def _sanitize(self, text):
        """ Sanitize text, removing markup tags and

        Parameters
        ----------
        text: str
              text to be sanitized

        Returns
        -------
        str
             Sanitized text
        """
        text = self._clean_wikimarkup(text)
        text = self._remove_stopwords(text)

        return text

    def _clean_wikimarkup(self, text):
        """ Remove all wikimarkup from the text

        Parameters
        ----------
        text: str
             text to remove wikimarkup from

        Returns
        -------
        str
             Sanitized text
        """

        # TODO: Dumb cleaning of Wikitext formatting, find a better way to clean text
        # text to lowercase and remove white trailing spaces
        text = text.lower().strip()
        text = re.sub("&.{2,4};", " ", text)
        text = re.sub("\\{\\{!\\}\\}", " ", text)
        # Remove text in the format {{ ... }}
        text = re.sub("{{.*?}}", "", text)
        # Remove markup tags in the format <foo> OR </foo>
        text = re.sub("<.*?>", "", text)
        # remove all non alphanumeric characters
        text = re.sub("[^a-z0-9çáéíóúàãõâêô-]", " ", text)

        return text

    def _remove_stopwords(self, text):
        """ Sanitize text, removing stopwords

        Parameters
        ----------
        text: str
              text to remove stopwords from

        Returns
        -------
        str
             Sanitized text
        """

        return " ".join(word for word in text.split() if word not in self._stopwords)


class QueryParser:

    def __init__(self, filename):
        self._filename = filename
        self._queries = []

        self.parse()  # execute the parse of queries

    def parse(self):
        with open(self._filename) as f:
            lines = ''.join(f.readlines())
        self._queries = [x.strip().split() for x in lines.split('\n')[:-1]]

    @property
    def queries(self):
        return self._queries

if __name__ == '__main__':
    qp = QueryParser('../text/queries.txt')
    print (qp.queries)
    # cp = CorpusParser('../text/ptwiki-v2.trec.xml', '../text/stopwords')
