from sympy import root
import math
import random as rnd
import numpy as np
import requests
from collections import Counter

# exponentiation modulaire
def modular_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# inverse multiplicatif de a modulo m
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Pas d'inverse multiplicatif")
    else:
      return x % m
    
# convert string to list of integer
def str_to_int_list(x):
  z = [ord(a) for a in x  ]
  for x in z:
    if x > 256:
      print(x)
      return False
  return z

# convert a strint to an integer
def str_to_int(x):
  x = str_to_int_list(x)
  if x == False:
    print("Le text n'est pas compatible!")
    return False

  res = 0
  for a in x:
    res = res * 256 + a
  i = 0
  res = ""
  for a in x:
    ci = "{:08b}".format(a )
    if len(ci)>8:
      print()
      print("long",a)
      print()
    res = res + ci
  res = eval("0b"+res)
  return res

def encodedIntToString(message):
    message = bin(message)
    message = message[2:] #remove 0b
    zeroToAdd = ((8 - len(message) % 8) % 8) * "0"
    message = zeroToAdd + message

    letter = ""
    word = ""
    for x in message:
        if len(letter) == 8:
            letter = int(letter, 2)
            letter = chr(letter)
            word += letter
            letter = ""
        letter += x
    letter = int(letter, 2)
    letter = chr(letter)
    word += letter
    return(word)

# Clé publique Question 1.2
N = 172219604291138178634924980176652297603347655313304280071646410523864939208855547078498922947475940487766894695848119416017067844129458299713889703424997977808694983717968420001033168722360067307143390485095229367172423195469582545920975539060699530956357494837243598213416944408434967474317474605697904676813343577310719430442085422937057220239881971046349315235043163226355302567726074269720408051461805113819456513196492192727498270702594217800502904761235711809203123842506621973488494670663483187137290546241477681096402483981619592515049062514180404818608764516997842633077157249806627735448350463
e = 173

# Cryptogramme 1.2
C = 25782248377669919648522417068734999301629843637773352461224686415010617355125387994732992745416621651531340476546870510355165303752005023118034265203513423674356501046415839977013701924329378846764632894673783199644549307465659236628983151796254371046814548224159604302737470578495440769408253954186605567492864292071545926487199114612586510433943420051864924177673243381681206265372333749354089535394870714730204499162577825526329944896454450322256563485123081116679246715959621569603725379746870623049834475932535184196208270713675357873579469122917915887954980541308199688932248258654715380981800909

names = [
    "Michel Houellebecq",
    "Christian Bobin",
    "Kazuo Ishiguro",
    "Ernest Hemingway",
    "Stendhal",
    "Joseph Roth",
    "Patrick Modiano",
    "Yukio Mishima",
    "Günter Grass",
    "Mikhaïl Boulgakov",
    "Ievgueni Zamiatine",
    "Sofi Oksanen",
    "Maxime Gorki",
    "Stig Dagerman",
    "Danilo Kis",
    "Chateaubriand",
    "Amos Oz",
    "Denis Diderot",
    "Michael Cunningham",
    "Malcolm Lowry",
    "James Joyce",
    "Alice Munro",
    "Jonathan Franzen",
    "John Banville",
    "Per Petterson",
    "Enrique Vila-Matas",
    "Edouard Limonov",
    "Ivan Tourgueniev",
    "Patrick Süskind",
    "Carson McCullers",
    "Knut Hamsun",
    "Julio Cortázar",
    "F. Scott Fitzgerald",
    "Nicolas Gogol",
    "Jean-Paul Sartre",
    "Albert Camus",
    "Charlotte Brontë",
    "Honoré de Balzac",
    "Nathaniel Hawthorne",
    "Anton Tchekhov",
    "Alexandre Pouchkine",
    "Oscar Wilde",
    "Heinrich von Kleist",
    "Mary Shelley",
    "Bram Stoker",
    "Italo Svevo",
    "Hermann Hesse",
    "Philip K. Dick",
    "Joseph Conrad",
    "J.M. Coetzee",
    "Anthony Burgess",
    "Imre Kertész",
    "Saul Bellow",
    "Franz Kafka",
    "Orhan Pamuk",
    "Stefan Zweig",
    "Ivan Gontcharov",
    "Émile Zola",
    "Alexandre Dumas",
    "Herta Müller",
    "J.M.G. Le Clézio",
    "Henry Fielding",
    "Peter Handke",
    "Thomas Mann",
    "W.G. Sebald",
    "Pietro Citati",
    "Gao Xingjian",
    "Milan Kundera",
    "William Faulkner",
    "Charles Dickens",
    "Benjamin Constant",
    "Haruki Murakami",
    "Mo Yan",
    "Henry James",
    "Paul Auster",
    "George Orwell",
    "Jorge Luis Borges",
    "Céline",
    "Thomas Bernhard",
    "Herman Melville",
    "George Eliot",
    "Victor Hugo",
    "Gustave Flaubert",
    "Cormac McCarthy",
    "Don DeLillo",
    "Elfriede Jelinek",
    "Philip Roth",
    "José Saramago",
    "Marcel Proust",
    "Fernando Pessoa",
    "Miguel de Cervantes",
    "Léon Tolstoï",
    "Johann Wolfgang von Goethe",
    "Robert Walser",
    "Robert Musil",
    "Virginia Woolf",
    "Vladimir Nabokov",
    "Fiodor Dostoïevski",
    "Roberto Bolaño",
    "Samuel Beckett"
]

for name in names:
   
  nbEncode = str_to_int(name)

  nbcrypte = modular_pow(nbEncode, e, N)

  if(nbcrypte == C):
    print("Message trouvé: ", name)
    break
else:
   print("Message non trouvé")
