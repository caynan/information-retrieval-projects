package org.caynan;
//
//import java.util.HashMap;
//import java.util.StringJoiner;
//

import org.apache.lucene.analysis.br.BrazilianAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;

import java.io.IOException;
import java.util.List;


/**
 * Created by caynan on 8/5/16.
 */
public class Index {
    private IndexWriter index;

    public Index() throws IOException {
        Directory dir = new RAMDirectory();
        IndexWriterConfig config = new IndexWriterConfig(new BrazilianAnalyzer())
                .setSimilarity(new BM25Similarity());
        // Set to use Okapi BM25 model
        index = new IndexWriter(dir, config);
    }

    public void populateIndex(List<WikiArticle> articles) throws IOException {
        for (WikiArticle article: articles) {
            Document doc = new Document();
            doc.add(new StringField("docId", article.getDocId(), Field.Store.YES));
            doc.add(new StringField("title", article.getTitle(), Field.Store.YES));
            doc.add(new TextField("body", article.getCorpus(), Field.Store.NO));

            index.addDocument(doc);
        }
    }

    public void search(String searchQuery, int n) throws IOException, ParseException{
        QueryParser qp = new QueryParser("body", new BrazilianAnalyzer());
        IndexSearcher searcher = new IndexSearcher(DirectoryReader.open(index));
        Query query = qp.parse(searchQuery);
        TopDocs topDocs = searcher.search(query, n);
        ScoreDoc[] hits = topDocs.scoreDocs;
        for (int i = 0; i < hits.length; i++) {
            Document doc = searcher.doc(hits[i].doc);
            System.out.println(doc.get("docId") + " - " + doc.get("title"));
        }
    }

}



//    private HashMap<String, HashMap<String, Integer>> index;
//    private Double meanDocumentLength;
//    private Integer indexedDocuments;
//
//
//    public Index() {
//        this.index = new HashMap<String, HashMap<String, Integer>>();
//        this.meanDocumentLength = 0.0;
//        this.indexedDocuments = 0;
//    }
//
//    public void addToken(String token, String docId) {
//        HashMap<String, Integer> docs = this.index.get(token);
//        if (docs != null) {
//            Integer termFrequency = (docs.get(docId) != null) ? docs.get(docId) : 0;
//            // Update the count for term frequency
//            this.index.get(token).put(docId, ++termFrequency);
//        } else {
//            HashMap<String, Integer> newDoc = new HashMap<>();
//            newDoc.put(docId, 1);
//            // insert new token to index
//            this.index.put(token, newDoc);
//        }
//    }
//
//    public void addDocument(Document doc) {
//        // Update the count of documents
//        this.indexedDocuments++;
//        // Update the documents mean length
//        this.setRunningMean(doc.length());
//
//        // Add token from document to our inverted index
//        String docId = doc.getDocId();
//        for (String token: doc) {
//            addToken(token, docId);
//        }
//    }
//
//    private void setRunningMean(Integer docLength) {
//        Double newMean = this.meanDocumentLength + ((docLength - this.meanDocumentLength) / indexedDocuments);
//        this.meanDocumentLength = newMean;
//    }
//
//    public Integer getTermFrequency(String token, String docId) throws NullPointerException {
//        HashMap<String, Integer> docs = this.index.get(token);
//        // we have the given token on the index
//        if (docs != null) {
//            Integer termFrequency = docs.get(docId);
//            // we have entries for the given token on the given index
//            if (termFrequency != null) {
//                return termFrequency;
//            }
//            else {
//                throw new NullPointerException(String.format("docId %s not found", docId));
//            }
//        }
//        else {
//            throw new NullPointerException(String.format("token %s not found", token));
//        }
//    }
//
//    public Integer getIndexFrequency(String token) {
//        HashMap<String, Integer> docs = this.index.get(token);poke go colabo
//        if (docs != null) {
//            return docs.size();
//        } else {
//            throw new NullPointerException(String.format("token %s not found", token));
//        }
//    }
//
