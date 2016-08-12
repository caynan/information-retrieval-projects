package org.caynan;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;


/**
 * Created by caynan on 8/12/16.
 */

public class Parser {
    // DOM Builder factory
    DocumentBuilderFactory factory;
    // DOM Builder
    DocumentBuilder builder;

    // WikiArticle List
    List<WikiArticle> wikiArticleList;


    public Parser(InputStream xmlStream) throws ParserConfigurationException, IOException, SAXException, ClassNotFoundException {
        this.factory = DocumentBuilderFactory.newInstance();
        this.builder = factory.newDocumentBuilder();
        // Create document from XML dump
        Document document = builder.parse(xmlStream);
        document.getDocumentElement().normalize();

        // Fill wikiArticleList with articles found on DUMP
        this.wikiArticleList = this.fillWikiArticle(document);
    }


    public List<WikiArticle> getArticles() {
        return this.wikiArticleList;
    }


    private List<WikiArticle> fillWikiArticle(Document document) {
        // List of WikiArticles
        List<WikiArticle> wikiArticles = new ArrayList<>();

        // Iterate over the nodes and extract the data
        NodeList nodeList = document.getElementsByTagName("DOC");

        for (int i = 0; i < nodeList.getLength(); i++)  {
            Node node = nodeList.item(i);
            if (node.getNodeType() == Node.ELEMENT_NODE) {
                Element element = (Element) node;
                // Article info
                String docId = element
                        .getElementsByTagName("DOCNO")
                        .item(0)
                        .getTextContent();
                String title = element
                        .getElementsByTagName("HEADLINE")
                        .item(0)
                        .getTextContent();

                String rawCorpus = element
                        .getElementsByTagName("P")
                        .item(0)
                        .getTextContent();

                // Clean Corpus
                String corpus = this.cleanCorpus(rawCorpus);

                // Create article and Add it to our list of articles
                WikiArticle article = new WikiArticle(docId, title, corpus);
                wikiArticles.add(article);
            }
        }

        return wikiArticles;
    }

    private String cleanCorpus(String rawCorpus) {
        rawCorpus = rawCorpus.toLowerCase();
        rawCorpus = rawCorpus.replaceAll("&.{2,4};", " ");
        rawCorpus = rawCorpus.replaceAll("\\{\\{!\\}\\}", " ");
        rawCorpus = rawCorpus.replaceAll("\\{\\{.*?\\}\\}", " ");
        rawCorpus = rawCorpus.replaceAll("<.*?>>", "");
        rawCorpus = rawCorpus.replaceAll("[^a-z0-9çáéíóúàãõâêô-]", " ");

        return rawCorpus;
    }
}

