from crypt import *
import math
import random as rnd
import numpy as np
import requests
from collections import Counter

def cut_string_into_pairs(text):
  pairs = []
  for i in range(0, len(text) - 1, 2):
    pairs.append(text[i:i + 2])
  if len(text) % 2 != 0:
    pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
  return pairs

def load_text_from_web(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while loading the text: {e}")
    return None


def gen_key(symboles):

  l=len(symboles)
  if l > 256:
    return False

  rnd.seed(1337)
  int_keys = rnd.sample(list(range(l)),l)
  dictionary = dict({})
  for s,k in zip(symboles,int_keys):
    dictionary[s]="{:08b}".format(k )
  return dictionary


def chiffrer(M,K, custom_dict):
  l = M_vers_symboles(M, K, custom_dict)
  l = [K[x] for x in l]
  return ''.join(l)


def M_vers_symboles(M, K, dictionaire):
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in dictionaire:
                encoded_text.append(pair)
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in K:
            encoded_text.append(M[i])
        else:
            # Conserve le caractère tel quel si non trouvé
            encoded_text.append(M[i])
        i += 1

    return encoded_text



def load_corpus():
    url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
    text = load_text_from_web(url)
    url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
    corpus = text + load_text_from_web(url)
    return corpus


def decrypt(C):
   MessageLonguer = len(C)/8
   MaxSymbol = 6000
   if MessageLonguer > MaxSymbol:
      M = decryptLongTest(C) # Methode frequent analysis
   else:   
      M = bruteForce(C) #Methode BruteFOrce

   return M
    
    



#Methode 1 Brute Force
def bruteForce(C):
   corpus = load_corpus()
   K = {'b': '10111011', 'j': '10010010', '\r': '10010101', 'J': '11111111', '”': '00101010', ')': '11000110', 'Â': '11010011', 'É': '01010101', 'ê': '01100010', '5': '10100010', 't': '11001010', '9': '01011100', 'Y': '11101011', '%': '01001110', 'N': '01100100', 'B': '10110010', 'V': '00110100', '\ufeff': '11000010', 'Ê': '10101000', '?': '11011101', '’': '11101001', 'i': '01011101', ':': '00011011', 's': '01101100', 'C': '11010010', 'â': '11110110', 'ï': '01100110', 'W': '00010000', 'y': '10000001', 'p': '11110000', 'D': '10101011', '—': '01011001', '«': '01100111', 'º': '11011111', 'A': '11001101', '3': '10111100', 'n': '11001100', '0': '01001111', 'q': '10101001', '4': '00000100', 'e': '11010101', 'T': '01011010', 'È': '10011000', '$': '00011110', 'U': '01110101', 'v': '00111111', '»': '00101011', 'l': '11001011', 'P': '01010000', 'X': '10101101', 'Z': '10110000', 'À': '10011010', 'ç': '11111001', 'u': '11011011', '…': '01000011', 'î': '00110011', 'L': '10001100', 'k': '00010001', 'E': '10100011', 'R': '10000110', '2': '10011110', '_': '10010011', '8': '00001011', 'é': '00010010', 'O': '01101000', 'Î': '10100111', '‘': '11000011', 'a': '00001101', 'F': '10101100', 'H': '11011000', 'c': '11100110', '[': '00110010', '(': '10111000', "'": '00011010', 'è': '01001000', 'I': '10110111', '/': '01110011', '!': '10010001', ' ': '11001111', '°': '00000011', 'S': '10011100', '•': '11111000', '#': '01101110', 'x': '11111110', 'à': '00111010', 'g': '11000111', '*': '11000001', 'Q': '10001110', 'w': '10100101', '1': '11110010', 'û': '00110110', '7': '10101111', 'G': '00101110', 'm': '10000111', '™': '11000100', 'K': '10111001', 'z': '00101111', '\n': '00001100', 'o': '01111110', 'ù': '11111101', ',': '01110100', 'r': '00000110', ']': '10000101', '.': '01111100', 'M': '10001010', 'Ç': '11010110', '“': '11101101', 'h': '11100010', '-': '01000001', 'f': '11001001', 'ë': '11111010', '6': '00100001', ';': '00001111', 'd': '11010001', 'ô': '10110001', 'e ': '00010100', 's ': '00110001', 't ': '01110000', 'es': '01000000', ' d': '11011100', '\r\n': '00100110', 'en': '01101101', 'qu': '11100000', ' l': '00001010', 're': '11001110', ' p': '01001001', 'de': '00100111', 'le': '00001110', 'nt': '01110110', 'on': '00101100', ' c': '00110000', ', ': '00001000', ' e': '10110110', 'ou': '00101101', ' q': '01010100', ' s': '01010110', 'n ': '01010010', 'ue': '01001100', 'an': '10010000', 'te': '01011011', ' a': '11110011', 'ai': '00011000', 'se': '10010100', 'it': '00111101', 'me': '10110100', 'is': '10100110', 'oi': '10111110', 'r ': '01000110', 'er': '00100000', ' m': '10101010', 'ce': '00011100', 'ne': '10011011', 'et': '11111011', 'in': '01101111', 'ns': '11011010', ' n': '01110010', 'ur': '01100001', 'i ': '01100101', 'a ': '00110101', 'eu': '01101010', 'co': '10111111', 'tr': '00111100', 'la': '11110111', 'ar': '10011001', 'ie': '10001101', 'ui': '00101001', 'us': '00000101', 'ut': '11101100', 'il': '01000101', ' t': '01111111', 'pa': '11110001', 'au': '01110111', 'el': '00110111', 'ti': '11100011', 'st': '01010111', 'un': '00101000', 'em': '11001000', 'ra': '01111010', 'e,': '01101001', 'so': '01111001', 'or': '00111000', 'l ': '01001010', ' f': '01111101', 'll': '10000010', 'nd': '11000000', ' j': '00100011', 'si': '11010100', 'ir': '10001011', 'e\r': '10000100', 'ss': '11100001', 'u ': '00000000', 'po': '10100100', 'ro': '11111100', 'ri': '01100011', 'pr': '00111011', 's,': '01110001', 'ma': '00011111', ' v': '11010000', ' i': '11101111', 'di': '10100000', ' r': '10101110', 'vo': '11010111', 'pe': '00000010', 'to': '01101011', 'ch': '00100101', '. ': '01010011', 've': '10111101', 'nc': '01011111', 'om': '01001101', ' o': '00000111', 'je': '11011110', 'no': '10001111', 'rt': '00010011', 'à ': '01011000', 'lu': '10010111', "'e": '10001000', 'mo': '00010110', 'ta': '00100010', 'as': '00010101', 'at': '01011110', 'io': '11110101', 's\r': '00001001', 'sa': '00111001', "u'": '00111110', 'av': '10010110', 'os': '01001011', ' à': '11101110', ' u': '10111010', "l'": '10011111', "'a": '10000000', 'rs': '01000010', 'pl': '01100000', 'é ': '00010111', '; ': '10001001', 'ho': '10011101', 'té': '01111011', 'ét': '00011101', 'fa': '11110100', 'da': '11101000', 'li': '01000111', 'su': '11000101', 't\r': '01000100', 'ée': '10000011', 'ré': '11100111', 'dé': '01111000', 'ec': '11100101', 'nn': '11101010', 'mm': '01010001', "'i": '00100100', 'ca': '11100100', 'uv': '00011001', '\n\r': '10100001', 'id': '11011001', ' b': '10110011', 'ni': '00000001', 'bl': '10110101'}

   custom_dict = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

   cryptoPattern = cryptToPattern(C)
   lettersInCryptogram = len(C) // 8
   print(lettersInCryptogram)
   i = 0
   while i <= len(corpus) - len(cryptoPattern):
        x = i
        while x < i + lettersInCryptogram * 2:
            
            corpuscrypted = chiffrer(corpus[i:x + lettersInCryptogram], K, custom_dict)
            corpusPattern = cryptToPattern(corpuscrypted)
            print("x: "+ str(x) + " i: " + str(i))
            if corpusPattern[0:50] != cryptoPattern[0:50]:
                break
            if corpusPattern == cryptoPattern:
                return corpus[i:x + lettersInCryptogram]
            x += 1
        i += 1
   return "Not found"


def cryptToPattern(cryptogram):
    i = 0
    symbol  = ""
    symbolTab = []
    pattern = ""
    while i < len(cryptogram):
        symbol += cryptogram[i]
        if len(symbol) == 8:
            if symbol not in symbolTab:
                pattern += (str(len(symbolTab))) + ","
                symbolTab.append(symbol)
                symbol = ""
            else:
                pattern += str(symbolTab.index(symbol)) + ","
                symbol = ""
        i += 1
    return pattern




#Methode 2 frequent analysis  matching 

def decryptLongTest(C):
   corpus = load_corpus()
   custom_dict = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
   K = {'b': '10111011', 'j': '10010010', '\r': '10010101', 'J': '11111111', '”': '00101010', ')': '11000110', 'Â': '11010011', 'É': '01010101', 'ê': '01100010', '5': '10100010', 't': '11001010', '9': '01011100', 'Y': '11101011', '%': '01001110', 'N': '01100100', 'B': '10110010', 'V': '00110100', '\ufeff': '11000010', 'Ê': '10101000', '?': '11011101', '’': '11101001', 'i': '01011101', ':': '00011011', 's': '01101100', 'C': '11010010', 'â': '11110110', 'ï': '01100110', 'W': '00010000', 'y': '10000001', 'p': '11110000', 'D': '10101011', '—': '01011001', '«': '01100111', 'º': '11011111', 'A': '11001101', '3': '10111100', 'n': '11001100', '0': '01001111', 'q': '10101001', '4': '00000100', 'e': '11010101', 'T': '01011010', 'È': '10011000', '$': '00011110', 'U': '01110101', 'v': '00111111', '»': '00101011', 'l': '11001011', 'P': '01010000', 'X': '10101101', 'Z': '10110000', 'À': '10011010', 'ç': '11111001', 'u': '11011011', '…': '01000011', 'î': '00110011', 'L': '10001100', 'k': '00010001', 'E': '10100011', 'R': '10000110', '2': '10011110', '_': '10010011', '8': '00001011', 'é': '00010010', 'O': '01101000', 'Î': '10100111', '‘': '11000011', 'a': '00001101', 'F': '10101100', 'H': '11011000', 'c': '11100110', '[': '00110010', '(': '10111000', "'": '00011010', 'è': '01001000', 'I': '10110111', '/': '01110011', '!': '10010001', ' ': '11001111', '°': '00000011', 'S': '10011100', '•': '11111000', '#': '01101110', 'x': '11111110', 'à': '00111010', 'g': '11000111', '*': '11000001', 'Q': '10001110', 'w': '10100101', '1': '11110010', 'û': '00110110', '7': '10101111', 'G': '00101110', 'm': '10000111', '™': '11000100', 'K': '10111001', 'z': '00101111', '\n': '00001100', 'o': '01111110', 'ù': '11111101', ',': '01110100', 'r': '00000110', ']': '10000101', '.': '01111100', 'M': '10001010', 'Ç': '11010110', '“': '11101101', 'h': '11100010', '-': '01000001', 'f': '11001001', 'ë': '11111010', '6': '00100001', ';': '00001111', 'd': '11010001', 'ô': '10110001', 'e ': '00010100', 's ': '00110001', 't ': '01110000', 'es': '01000000', ' d': '11011100', '\r\n': '00100110', 'en': '01101101', 'qu': '11100000', ' l': '00001010', 're': '11001110', ' p': '01001001', 'de': '00100111', 'le': '00001110', 'nt': '01110110', 'on': '00101100', ' c': '00110000', ', ': '00001000', ' e': '10110110', 'ou': '00101101', ' q': '01010100', ' s': '01010110', 'n ': '01010010', 'ue': '01001100', 'an': '10010000', 'te': '01011011', ' a': '11110011', 'ai': '00011000', 'se': '10010100', 'it': '00111101', 'me': '10110100', 'is': '10100110', 'oi': '10111110', 'r ': '01000110', 'er': '00100000', ' m': '10101010', 'ce': '00011100', 'ne': '10011011', 'et': '11111011', 'in': '01101111', 'ns': '11011010', ' n': '01110010', 'ur': '01100001', 'i ': '01100101', 'a ': '00110101', 'eu': '01101010', 'co': '10111111', 'tr': '00111100', 'la': '11110111', 'ar': '10011001', 'ie': '10001101', 'ui': '00101001', 'us': '00000101', 'ut': '11101100', 'il': '01000101', ' t': '01111111', 'pa': '11110001', 'au': '01110111', 'el': '00110111', 'ti': '11100011', 'st': '01010111', 'un': '00101000', 'em': '11001000', 'ra': '01111010', 'e,': '01101001', 'so': '01111001', 'or': '00111000', 'l ': '01001010', ' f': '01111101', 'll': '10000010', 'nd': '11000000', ' j': '00100011', 'si': '11010100', 'ir': '10001011', 'e\r': '10000100', 'ss': '11100001', 'u ': '00000000', 'po': '10100100', 'ro': '11111100', 'ri': '01100011', 'pr': '00111011', 's,': '01110001', 'ma': '00011111', ' v': '11010000', ' i': '11101111', 'di': '10100000', ' r': '10101110', 'vo': '11010111', 'pe': '00000010', 'to': '01101011', 'ch': '00100101', '. ': '01010011', 've': '10111101', 'nc': '01011111', 'om': '01001101', ' o': '00000111', 'je': '11011110', 'no': '10001111', 'rt': '00010011', 'à ': '01011000', 'lu': '10010111', "'e": '10001000', 'mo': '00010110', 'ta': '00100010', 'as': '00010101', 'at': '01011110', 'io': '11110101', 's\r': '00001001', 'sa': '00111001', "u'": '00111110', 'av': '10010110', 'os': '01001011', ' à': '11101110', ' u': '10111010', "l'": '10011111', "'a": '10000000', 'rs': '01000010', 'pl': '01100000', 'é ': '00010111', '; ': '10001001', 'ho': '10011101', 'té': '01111011', 'ét': '00011101', 'fa': '11110100', 'da': '11101000', 'li': '01000111', 'su': '11000101', 't\r': '01000100', 'ée': '10000011', 'ré': '11100111', 'dé': '01111000', 'ec': '11100101', 'nn': '11101010', 'mm': '01010001', "'i": '00100100', 'ca': '11100100', 'uv': '00011001', '\n\r': '10100001', 'id': '11011001', ' b': '10110011', 'ni': '00000001', 'bl': '10110101'}
   chiffrageDuCComplete = chiffrer(corpus, K, K)
   decryptageVite = frequentDecrypt(chiffrageDuCComplete,corpus,custom_dict, C)

   

   return decryptageVite





def frequentDecrypt(texteChiffre, corpus, symboles, texteOriginal, longueurSegment=8):
    listeSegmentsChiffres = []
    longueurTotaleTexteChiffre = len(texteChiffre)
    indexDepart = 0
    
    while indexDepart < longueurTotaleTexteChiffre:
        indexFin = indexDepart + longueurSegment
        segmentActuel = texteChiffre[indexDepart:indexFin]
        listeSegmentsChiffres.append(segmentActuel)
        indexDepart += longueurSegment
    # Analyse
    segmentsChiffre = listeSegmentsChiffres
    frequenceSegmentsChiffre = Counter(segmentsChiffre)
    
    symbolesReference = M_vers_symboles(corpus, symboles, symboles)
    distributionFrequenceReference = Counter(symbolesReference)

    symbolesReferenceTries = sort_frequency(distributionFrequenceReference)
    segmentsChiffreTries = sort_frequency(frequenceSegmentsChiffre)

    cleSuppositionInversee = {}
    min_length = min(len(symbolesReferenceTries), len(segmentsChiffreTries))

    for i in range(min_length):
      symbole = symbolesReferenceTries[i][0]   
      segment = segmentsChiffreTries[i][0]   
      cleSuppositionInversee[symbole] = segment

    segmentsTexteOriginal = []
    longueurTotaleTexteOriginal = len(texteOriginal)
    indexDepartTexte = 0
    
    while indexDepartTexte < longueurTotaleTexteOriginal:
        indexFinTexte = indexDepartTexte + longueurSegment
        segmentTexte = texteOriginal[indexDepartTexte:indexFinTexte]
        segmentsTexteOriginal.append(segmentTexte)
        indexDepartTexte += longueurSegment
    #dechiffrage
    listeSymbolesDechiffres = []

    for segmentTexte in segmentsTexteOriginal:
        symboleCorrespondant = '?'
        for cleSupposition, valeurSegment in cleSuppositionInversee.items():
            if valeurSegment == segmentTexte:
                symboleCorrespondant = cleSupposition
                break  # Sortir de la boucle dès qu'une correspondance est trouvée

        listeSymbolesDechiffres.append(symboleCorrespondant)

    texteDechiffreFinal = ''.join(listeSymbolesDechiffres)

    return texteDechiffreFinal
def sort_frequency(freq_dict):

    if isinstance(freq_dict, Counter):
        return freq_dict.most_common()
    else:
        return Counter(freq_dict).most_common()

