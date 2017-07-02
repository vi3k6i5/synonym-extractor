
synonym-extractor
==============

Why
-----

Say you have a corpus where similar words appear very frequently.
eg: Last weekened I was in NY.
    I am traveling to new york next weekend.

If you train a word2vec model on this or do any sort of NLP it will treat NY and ney york as 2 different words. Instead if you create a synonym dictionary like:
eg: NY=>new york
    new york=>new york
then you can extract NY and new york as the same text.

If you are thinking this can be done with a simple regex, you are right.
I was doing this with a regex for a long time.

My corpus was 1.5 Million docs and 2K synonyms. It used to take python approx 16 hours to process through.

Recently my corpus went up to 2.5 Million docs and some 10K plus synonyms. Now it was going to take me 15 days to process.

With this library I am able to process 2.5M docs and 10K synonyms in 15 mins.

The idea for this library came from the following `StackOverflow question
<https://stackoverflow.com/questions/44178449/regex-replace-is-taking-time-for-millions-of-documents-how-to-make-it-faster>`_.


Installation
-------
::

    pip install synonym-extractor

Usage
------
::
    
    # import module
    from synonym.extractor import SynonymExtractor

    # Create an object of SynonymExtractor
    synonym_extractor = SynonymExtractor()

    # add synonyms to it
    synonym_names = ['NY', 'SF']
    clean_names = ['new york', 'san francisco']

    for synonym_name, clean_name in zip(synonym_names, clean_names):
        synonym_extractor.add_to_synonym(synonym_name, clean_name)

    synonyms_found = synonym_extractor.get_synonyms_from_sentence('I love SF and NY')

    synonyms_found
    >> ['san francisco', 'new york']

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
