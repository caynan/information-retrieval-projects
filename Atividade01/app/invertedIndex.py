import xml.etree.ElementTree as ET
import json
import re
import gzip
import shutil

from collections import defaultdict

#TODO: implement abstract class for index type (must implement search method that return a searchResult object)
class InvertedIndex:
    """An Inverted index, it can be created using a wikipedia dump

    Attributes:
        index: dict
             Inverted index created from the given dump_filepath
    """

    def __init__(self, dump_filepath, stopword_filepath='stopwords.txt'):
        """ Tokenize an wikipedia XML Dump

        Parameters
        ----------
        dump_filepath: str
              filepath for the xml dump to be processed
        stopword_filepath: str
              filepath for stopwords (file must contain one  stopword per line)
        """
        self._stopwords = set(open(stopword_filepath).read().split())
        self._corpus = self._tokenize(dump_filepath)
        self._index = self._create_index(self._corpus)

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
        # transform index to be a dict of list not sets (since json don't support sets)
        temp_index = {token: list(docs) for (token, docs) in self.index.items()}
        # add json extention to filepath
        filepath = filename + ".json"

        if compressed:
            filepath += ".gz"
            with gzip.open(filepath, mode="wt") as json_file:
                json.dump(temp_index, json_file, ensure_ascii=False, sort_keys=True, indent=4)
        else:
            with open(filepath, 'w', encoding='utf8') as json_file:
                json.dump(temp_index, json_file, ensure_ascii=False, sort_keys=True, indent=4)


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
