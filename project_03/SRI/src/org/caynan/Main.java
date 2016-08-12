package org.caynan;

import org.apache.lucene.queryparser.classic.ParseException;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        try {
            // TODO: Add option to receive file path from CLI
            File xmlDump = new File("/Users/caynan/Projects/UFCG/16.1/RI/Atividade01/data/ptwiki-v2.trec.xml");
            InputStream dumpStream = new FileInputStream(xmlDump);
            Parser parser = new Parser(dumpStream);
            List<WikiArticle> articles = parser.getArticles();

            Index index = new Index();
            index.populateIndex(articles);

            // TEST SEARCH

            try {
                index.search("Arara", 10);
            } catch (IOException e) {
                e.printStackTrace();
            } catch (ParseException e) {
                e.printStackTrace();
            }

//            System.out.println(articles.get(0));
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
