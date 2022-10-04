class Encryption():

    def __init__(self):
        self.original_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                              'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', ',', '.', '?', '/']
        text_file = open("Key.txt")
        data = text_file.read()
        self.encoded_list = [i for i in data]
        text_file.close()

    def encrypt(self, message):
        cipher_text = ""
        for message_char in message:
            if message_char in self.original_list:
                index = self.original_list.index(message_char)
                cipher_text += self.encoded_list[index]
            else:

                cipher_text += str(message_char)
                return cipher_text

    def decrypt(self, cipher_text):
        message = ""
        for cipher_char in cipher_text:
            if cipher_char in self.encoded_list:
                index = self.encoded_list.index(cipher_char)
                message += self.original_list[index]
            else:
                message += str(cipher_char)
        return message
