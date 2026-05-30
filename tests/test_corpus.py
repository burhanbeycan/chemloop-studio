from chemloop_studio.corpus import load_corpus


def test_load_corpus_has_documents():
    docs = load_corpus()
    assert len(docs) >= 5
    assert docs[0].doc_id
    assert docs[0].citation.endswith(")")
