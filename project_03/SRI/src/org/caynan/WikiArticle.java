package org.caynan;

/**
 * Created by caynan on 8/5/16.
 */

public class WikiArticle {
    private final String docId, title;
    private final Integer length;
    private final String corpus;

    public WikiArticle(String docId, String title, String corpus) {
        this.docId = docId;
        this.title = title;
        this.corpus = corpus;
        this.length = corpus.length();
    }

    public String getCorpus() {
        return this.corpus;
    }

    public String getDocId() {
        return this.docId;
    }

    public String getTitle() {
        return this.title;
    }

    public Integer length() {
        return this.length;
    }

    @Override
    public  String toString() {
        return String.format("id: %s\ttitle: %s\n%s", this.getDocId(), this.getTitle(), this.getCorpus());
    }
}
