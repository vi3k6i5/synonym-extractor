from synonym.extractor import SynonymExtractor


class TestSynonymExtractor(object):
    def setup_method(self, method):
        print("start testing")
        self.synonym_extractor = SynonymExtractor()
        synonym_names = ['javaee', 'j2ee', 'java']
        clean_names = ['java', 'java', 'java']
        for synonym_name, clean_name in zip(synonym_names, clean_names):
            self.synonym_extractor.add_to_synonym(synonym_name, clean_name)

    def teardown_method(self, method):
        print("end testing")

    def test_extract_synonyms(self):
        synonyms_found = self.synonym_extractor.get_synonyms_from_sentence('javaee is my language j2ee is my code')
        assert all(x in synonyms_found for x in ['java', 'java'])
