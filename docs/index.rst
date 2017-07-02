Welcome to Synonym Extractor's documentation!
=============================================


Synonym Extractor is a python library that based on `Aho-Corasick algorithm
<https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_.

The idea is to extract words that we care about from a given sentence in one pass.

Basically say I have a vocabulary of 10K words and I want to get all the words from that set present in a sentence. A simple regex match will take a lot of time to loop over the 10K documents.

Hence we use a simpler yet much faster algorithm to get the desired result.


Installation
------------
::

    pip install synonym-extractor

API Reference
-------------

.. module:: synonym.extractor

.. class:: SynonymExtractor()

    ``Usage``::

        # Create an object of SynonymExtractor
        synonym_extractor = SynonymExtractor()

        # add synonyms to it
        synonym_names = ['NY', 'SF']
        clean_names = ['new york', 'san francisco']

        for synonym_name, clean_name in zip(synonym_names, clean_names):
            synonym_extractor.add_to_synonym(synonym_name, clean_name)

        synonyms_found = synonym_extractor.get_synonyms_from_sentence('I love SF and NY')

    ``Output``::

        synonyms_found
        >> ['new york', 'san francisco']


    ``Define synonyms``::

        # There are 2 ways to define synonyms.

        # 1. Is to add to the synonym by calling this method

        synonym_extractor.add_to_synonym('madras', 'chennai')

        # 2. Pass a file path

        # Format supported is 
        #     madras=>chennai
        #     SF=>san francisco

        synonym_extractor.build_synonym('/file_path_to_synonyms.txt')


    Note: Synonyms are case sensitive. You will be adviced to lower case all text if you want case insensitive match.


    ``get synonyms from sentence``::

        # This method extracts all matching synonyms in the sentense and returns a list

        synonym_extractor.get_synonyms_from_sentence('i love NY')
        >> ['new york']

    ``change the internal white space characters``::

        synonym_extractor = SynonymExtractor()
        synonym_extractor._set_white_space_chars(set(['.', ' ']))


Contribute
----------

- Issue Tracker: https://github.com/vi3k6i5/synonym-extractor/issues
- Source Code: https://github.com/vi3k6i5/synonym-extractor/


License
-------

The project is licensed under the MIT license.