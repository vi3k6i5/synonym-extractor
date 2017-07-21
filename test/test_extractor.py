from synonym.extractor import SynonymExtractor


class TestSynonymExtractor(object):
    def setup_method(self, method):
        print("start testing")
        self.synonym_extractor = SynonymExtractor()
        synonym_names = ['NY', 'new-york', 'SF']
        clean_names = ['New York', 'New York', 'san francisco']
        for synonym_name, clean_name in zip(synonym_names, clean_names):
            self.synonym_extractor.add_to_synonym(synonym_name, clean_name)

    def teardown_method(self, method):
        print("end testing")

    def test_extract_synonyms(self):
        synonyms_found = self.synonym_extractor.get_synonyms_from_sentence('I love SF and Ny. New-york is the best.')
        assert all(x in synonyms_found for x in ['New York', 'san francisco'])
