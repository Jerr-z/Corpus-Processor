import PyPDF2,nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
from nltk.tokenize.treebank import TreebankWordDetokenizer
import json

nltk.download("punkt")
nltk.download("wordnet")


def extract_text(pdf_file: str) -> str:
  '''
  converts text in pdf into raw text
  '''
  with open(pdf_file, "rb") as pdf:
    #creates a reader object
    reader = PyPDF2.PdfReader(pdf, strict=False)
    text = ""
    for page in reader.pages:
      text += page.extract_text()
    return text

def extract_corpus(folder: str, dest: str) -> str:
  '''
  extracts text from a folder of pdfs

  lod: list of directory
  dest: save destination
  '''
  #list of directories
  lod = os.listdir(folder)

  for dir in lod:
    t = extract_text(folder+"/"+dir)
    print(dir)
    save_text_to_file(t, dest, "a")
  

def save_text_to_file(text: str, file: str, mode: str)-> None:
  '''
  saves string to file
  
  text: your text of choice
  file: destination file name
  mode: r, w, a etc...
  '''
  with open(file, mode) as f:
    for letter in text:
      f.writelines(letter)

def save_list_to_file(lst: list, file: str) -> None:
  '''
  saves a list to file with each element per line
  '''
  with open(file, "w") as f:
    for l in lst:
      f.writelines(l)
      f.writelines("\n")


def Lemmatize(tokens: [str]) -> [str]:
  '''
  Lemmatize a list of strings
  '''
  
  lemmatizer = WordNetLemmatizer()
  lemmas = []
  
  for l in tokens:
    lemma = lemmatizer.lemmatize(l)
    lemmas.append(lemma)
  return lemmas

def tokenize_los(los: [str]) -> [[str]]:
  '''
  los: a list of string
  
  tokenize a list of sentences
  '''
  rsf = []
  for s in los:
    rsf.append(word_tokenize(s))
  return rsf

def target_tokenized_sentence(lots: [[str]], keyword: str) -> [[str]]:
  '''
  lots: list of tokenized sentences
  keyword: the target word to find

  returns a list of tokenied sentences with the keyword
  '''
  rsf = []
  for ts in lots:
    if keyword in ts:
      rsf.append(ts)
  return rsf
      
def detokenize(los: [str]) -> str:
  '''
  detonkenizes a tokenized los
  '''

  detokenizer = TreebankWordDetokenizer()
  return detokenizer.detokenize(los)
  
#already extracted, commented out  
#extract_corpus("corpus articles", "corpora.txt")
#######################################################################################

def extract_asms(input,output):
  with open(input) as corpora:
    t = corpora.read()
    #print(corpora.read())
    
  #generates a list of sentences
  los = nltk.sent_tokenize(t)
  
  
  #list of tokenized sentences
  lots = tokenize_los(los)
  
  we_sentences = target_tokenized_sentence(lots, "we") + target_tokenized_sentence(lots, "We")
  our_sentences = target_tokenized_sentence(lots, "our") + target_tokenized_sentence(lots, "Our")
  
  for s in we_sentences:
    print(detokenize(s)+"\n")
    save_text_to_file(detokenize(s)+"\n", output, "a")
  
  for s in our_sentences:
    print(detokenize(s)+"\n")
    save_text_to_file(detokenize(s)+"\n", output, "a")

#extract_asms("corpora.txt", "we_sentences.txt")

def tabulate_asm_func(inputfile,output, d):
  with open(inputfile) as inp:
    sentences = inp.readlines()
  try:
    with open(d) as dictionary:
      dict = json.load(dictionary)
  except:
      dict = {}
  line=0
  for l in sentences:
    dict.setdefault("line", 0)
    if line<dict["line"]:
      line +=1
      continue
    line += 1
    print("Rhetorical Functions:\n 1. explaining experimental procedures \n 2. Presenting Opinion \n 3. Showing results and findings \n 4. Stating a goal or intention\n 5. none\n 6. q ")
    print(l)
    choice = input()
    if choice == 'q':
      break
    dict.setdefault(choice, 0)
    dict[choice]+=1
    dict["line"]+=1
  #TODO: dump
  with open(d,'w') as dfile:
    json.dump(dict,dfile)

#extract_asms("introductioncorpus.txt","we_intro.txt")
#tabulate_asm_func("we_intro.txt", "freq.json", "freq.json")
#extract_asms("r&d corpus.txt", "we_r&d.txt")
tabulate_asm_func("we_r&d.txt", "freq1.json", "freq1.json")