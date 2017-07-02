
synonym-extractor
==============

    ``Usage``::

        # Create an object of SynonymExtractor
        synonym_extractor = SynonymExtractor()

        # add synonyms to it
        synonym_names = ['javaee', 'j2ee', 'java']
        clean_names = ['java', 'java', 'java']

        for synonym_name, clean_name in zip(synonym_names, clean_names):
            synonym_extractor.add_to_synonym(synonym_name, clean_name)

        synonyms_found = synonym_extractor.get_synonyms_from_sentence('javaee is my language, j2ee is my code')

    ``Output``::

        synonyms_found
        >> ['java', 'java']

Algorithm
----------

synonym-extractor is based on `Aho-Corasick algorithm
<https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_.

Documentation
----------

Documentation can be found at `Read the Docs
<http://synonym-extractor.readthedocs.org>`_.

License
-------

The project is licensed under the MIT license.
