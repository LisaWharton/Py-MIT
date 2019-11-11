import string


### HELPER CODE ###
def load_words(inFile):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    with open('words.txt', 'r') as inFile:
        # wordlist: list of strings
        wordlist = []
        for line in inFile:
            wordlist.extend([word.lower() for word in line.split(' ')])
        print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    is_word(word_list, 'bat') returns
    True
    is_word(word_list, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        WordsList = self.valid_words
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return WordsList

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        list_ascii = list(string.ascii_lowercase)
        list_ascii_upper = list(string.ascii_uppercase)
        i = shift
        while i > 0:
            list_ascii.insert(0, list_ascii.pop())
            list_ascii_upper.insert(0, list_ascii_upper.pop())
            i -= 1
        string_ascii = "".join(list_ascii + list_ascii_upper)
        return dict(zip(string_ascii, string.ascii_lowercase + string.ascii_uppercase))

    def apply_shift(self, shift):
        ''' Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_words = []

        shift_dict = Message.build_shift_dict(self, shift)

        for letter in self.message_text:
            if letter in shift_dict:
                shifted_words.append(shift_dict[letter])
            else:
                shifted_words.append(letter)
        return "".join(shifted_words)


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # super().__init__(text)
        self.message_text = text
        self.valid_words = load_words('words.txt')
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, NewShift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = NewShift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        s = 26
        shift_count = [0]
        best_shift = [0]
        best_shift_message = []
        while s > 0:
            count = 0
            for word in Message.apply_shift(self, s).split():
                if word in self.valid_words:
                    count += 1
            if count == max(shift_count):
                shift_count.append(count)
                best_shift.append(26 - s)
                best_shift_message.append(Message.apply_shift(self, s))
            if count > max(shift_count):
                shift_count.append(count)
                best_shift.clear()
                best_shift.append(26 - s)
                best_shift_message.clear()
                best_shift_message.append(Message.apply_shift(self, s))
            s -= 1
        return best_shift, best_shift_message


if __name__ == '__main__':
    prompt = input('Enter the message you want to encrypt: ')
    import random

    shift = random.randint(1, 26)
    plaintext = PlaintextMessage(prompt, shift)
    print(plaintext.get_message_text_encrypted())
    print("")
    # encrypting the input message by a random shift value generated

    input('Click Enter to decrypt message: ')
    ciphertext = CiphertextMessage(plaintext.get_message_text_encrypted())
    print("")
    print('Output: Decryption shift value, Decrypted message:', ciphertext.decrypt_message())
    # decrypting the shift value and the encrypted input message
