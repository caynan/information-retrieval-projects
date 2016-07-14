class Search:
    """Object that store the result of a given search query

    Attributes:
        # index:
        #      Inverted index created from the given dump_filepath
    """

    def __init__(self, search_term, index):
        """Object that store the result of a given search query

        Attributes:
            search_term:
                 String that represent the search term
            index:
                 Index object that provide a search method.
        """
        self._search_term = search_term
        self._index = index
        # note: we're using sets to store our search result
        self._result = self._index.search(search_term)


    def __str__(self):
        return "{search_term} -> {results}".format(search_term=self._search_term, results=self._result)

    def __and__(self, other):
        """bitwise AND operation on the query result

        Attributes:
            query_a:
                 A Query object
            query_b:
                 A Query object
        """
        # note: O(len(query_a) * len(query_b)) see: https://wiki.python.org/moin/TimeComplexity
        return self._result & other._result

    def __or__(self, other):
        """bitwise OR operation on the query result
        Attributes:
            query_a:
                 A Query object
            query_b:
                 A Query object
        """
        # note: O(len(query_a) + len(query_b)) see: https://wiki.python.org/moin/TimeComplexity
        return self._result | other._result
