import os


class SynonymExtractor(object):
    """SynonymExtractor

    Parameters
    ----------
    case_sensitive : boolean, default False
        If you want the module to be case sensitive set it to True

    Attributes
    ----------
    `_end` : string, default '_end_'
        used to denote end of work in synonym_trie_dict
    `_synonym` : string, default '_synonym_'
        key in dict. used to store cleaned synonym name which will be returned
    `_white_space_chars` : set, default set(['.', '\t', '\n', '\a', ' '])
        values which will be used to identify if we have reached end of term
    `synonym_trie_dict` : dict, default {}
        trie dict built character by character, that is used for lookup
    `case_sensitive` : boolean, default False
        if the algorithm should be case sensitive or not

    Examples
    --------
    >>> # import module
    >>> from synonym.extractor import SynonymExtractor

    >>> # Create an object of SynonymExtractor
    >>> synonym_extractor = SynonymExtractor()

    >>> # add synonyms
    >>> synonym_names = ['NY', 'new-york', 'SF']
    >>> clean_names = ['new york', 'new york', 'san francisco']

    >>> for synonym_name, clean_name in zip(synonym_names, clean_names):
    >>>     synonym_extractor.add_to_synonym(synonym_name, clean_name)

    >>> synonyms_found = synonym_extractor.get_synonyms_from_sentence('I love SF and NY. new-york is the best.')

    >>> synonyms_found
    >>> ['san francisco', 'new york', 'new york']

    References
    ----------
    loosely based on https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm.
    Idea came from this question https://stackoverflow.com/questions/44178449/regex-replace-is-taking-time-for-millions-of-documents-how-to-make-it-faster
    """

    def __init__(self, case_sensitive=False):
        self._end = '_end_'
        self._synonym = '_synonym_'
        self._white_space_chars = set(['.', '\t', '\n', '\a', ' '])
        self.synonym_trie_dict = dict()
        self.case_sensitive = case_sensitive
        print("This project has been depricated. Please use FlashText https://github.com/vi3k6i5/flashtext instead.")

    def _set_white_space_chars(self, white_space_chars):
        """use this method if you want to replace the inbuilt white space chars
        Parameters
        ----------
        white_space_chars: set
            Set of characters that will be considered as whitespaces.
            This will denote that the term has ended.
        """
        self._white_space_chars = white_space_chars

    def add_to_synonym(self, synonym_name, clean_name):
        """
        if you want to add one or more synonym to the dictionary
        pass the synonym name and the clean name it maps to
        synonym_name: Name of the synonym
        clean_name: clean word
        Parameters
        ----------
        synonym_name : string
            keyword that you want to identify
        clean_name : string
            clean term for that keyword that you would want to get back in return
        """
        if synonym_name and clean_name:
            if not self.case_sensitive:
                synonym_name = synonym_name.lower()
            current_dict = self.synonym_trie_dict
            for letter in synonym_name:
                current_dict = current_dict.setdefault(letter, {})
            current_dict[self._synonym] = clean_name
            current_dict[self._end] = self._end

    def build_synonym(self, synonym_file):
        """
        if you want to add synonyms from a file
        synonym file format should be like:
        java_2e=>java
        java programing=>java
        product management=>product management
        product management techniques=>product management

        Parameters
        ----------
        synonym_file : path
        """
        if not os.path.isfile(synonym_file):
            raise("Invalid file path %s".format(synonym_file))
        with open(synonym_file)as f:
            for line in f:
                synonym_name, clean_name = line.split('=>')
                if not self.case_sensitive:
                    synonym_name = synonym_name.lower()
                self.add_to_synonym(unclean_name, clean_name.strip())

    def add_to_synonyms_from_dict(self, synonym_dict):
        """
        if you want to add synonyms from a dictionary
        Dict format should be like:
        {
            "java":["java_2e", "java programing"],
            "product management":["PM", "product manager"]
        }
        """
        for clean_name, synonym_names in synonym_dict.items():
            for synonym_name in synonym_names:
                if not self.case_sensitive:
                    synonym_name = synonym_name.lower()
                self.add_to_synonym(synonym_name, clean_name)

    def get_synonyms_from_sentence(self, sentence):
        """get synonyms from the input sentence.
        Parameters
        ----------
        sentence : string
            Line of text that you want to extract all terms from
        Returns
        -------
        synonyms_extracted : 1D array
            List of terms found in sentence
        """
        if not self.case_sensitive:
            sentence = sentence.lower()
        synonyms_extracted = []
        current_dict = self.synonym_trie_dict
        idx = 0
        sentence_len = len(sentence)
        while idx < sentence_len:
            char = sentence[idx]
            # when we reach whitespace
            if char in self._white_space_chars:

                # if end is present in current_dict
                if self._end in current_dict or char in current_dict:
                    # update longest sequence found
                    sequence_found = None
                    longest_sequence_found = None
                    if self._end in current_dict:
                        sequence_found = current_dict[self._synonym]
                        longest_sequence_found = current_dict[self._synonym]

                    # re look for longest_sequence from this position
                    if char in current_dict:
                        current_dict_continued = current_dict[char]

                        idy = idx + 1
                        while idy < sentence_len:
                            inner_char = sentence[idy]
                            if inner_char in current_dict_continued:
                                current_dict_continued = current_dict_continued[inner_char]
                            else:
                                break
                            if self._end in current_dict_continued:
                                # update longest sequence found
                                longest_sequence_found = current_dict_continued[self._synonym]
                            idy += 1
                        if longest_sequence_found != sequence_found:
                            idx = idy
                    current_dict = self.synonym_trie_dict
                    if longest_sequence_found:
                        synonyms_extracted.append(longest_sequence_found)

                else:
                    # we reset current_dict
                    current_dict = self.synonym_trie_dict
            elif char in current_dict:
                # we can continue from this char
                current_dict = current_dict[char]
            else:
                # we reset current_dict
                current_dict = self.synonym_trie_dict
                # skip to end of word
                idy = idx + 1
                while idy < sentence_len:
                    char = sentence[idy]
                    if char in self._white_space_chars:
                        break
                    idy += 1
                idx = idy
            # if we are end of sentence and have a sequence discovered
            if idx + 1 >= sentence_len:
                if self._end in current_dict:
                    sequence_found = current_dict[self._synonym]
                    synonyms_extracted.append(sequence_found)
            idx += 1
        return synonyms_extracted
