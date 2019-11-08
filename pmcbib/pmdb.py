from metapub import PubMedFetcher

tags = {'author', 'journal'}

def query_search(entry):
    pmids1 = fetch.pmids_for_citation(authors=entry['author'], journal=entry['journal'], year=entry['year'], volume=entry['volume'])
    pmids2 = fetch.pmids_for_query(entry['title'])

def search(entry):
    fetch = PubMedFetcher()
    try:
        article = fetch.article_by_pmid(entry['pmid'])
    except:
        try:
            article = fetch.article_by_pmcid(entry['pmcid'])
        except:
            try:
                article = fetch.article_by_doi(entry['doi'])
            except:
                try:
                    pmids = fetch.pmids_for_citation(authors=entry['author'], journal=entry['journal'], year=entry['year'], volume=entry['volume'])
                    # pmids2 = fetch.pmids_for_query(entry['title'])
                    article = fetch.article_by_pmid(pmids[0])
                except:
                    return None
    return article
