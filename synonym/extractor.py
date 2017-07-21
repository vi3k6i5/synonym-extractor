import os


class SynonymExtractor(object):

    def __init__(self):
        self._end = '_end_'
        self._synonym = '_synonym_'
        self._white_space_chars = set(['.', '\t', '\n', '\a', ' '])
        self.synonym_trie_dict = dict()

    """
    use this method if you want to replace the inbuilt white space chars
    """
    def _set_white_space_chars(self, white_space_chars):
        self._white_space_chars = white_space_chars

    """
        if you want to add one or more synonym to the dictionary
        pass the synonym name and the clean name it maps to
        synonym_name: Name of the synonym
        clean_name: clean word
    """
    def add_to_synonym(self, synonym_name, clean_name):
        if synonym_name and clean_name:
            current_dict = self.synonym_trie_dict
            for letter in synonym_name:
                current_dict = current_dict.setdefault(letter, {})
            current_dict[self._synonym] = clean_name
            current_dict[self._end] = self._end

    """
        if you want to add synonyms from a file
        synonym file format should be like:
        java_2e=>java
        java programing=>java
        product management=>product management
        product management techniques=>product management
    """
    def build_synonym(self, synonym_file):
        # build the synonyms
        if not os.path.isfile(synonym_file):
            raise("Invalid file path %s".format(synonym_file))
        with open(synonym_file)as f:
            for line in f:
                synonym_name, clean_name = line.split('=>')
                self.add_to_synonym(unclean_name, clean_name.strip())

    def get_synonyms_from_sentence(self, sentence):
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
