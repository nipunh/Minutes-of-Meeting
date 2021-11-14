from nltk import pos_tag
from nltk import RegexpParser


text ="Slap the CEO now".split()
print("After Split:",text)

tokens_tag = pos_tag(text)
print("After Token:",tokens_tag)

patterns = """mychunk:{<NN|NNP|PRP|PRP$|NNPS>+<DT|RB|RBR|RBS|VB|VBG|VBN|VBP|VBZ>*<VB|VBG|VBN|VBP|VBZ>*}"""

chunker = RegexpParser(patterns)
print("After Regex:",chunker)

output = chunker.parse(tokens_tag)
print("After Chunking",output)

# from nltk import pos_tag
# from nltk import RegexpParser
# text ="learn php from guru99 and make study easy".split()
# print("After Split:",text)
# tokens_tag = pos_tag(text)
# print("After Token:",tokens_tag)
# patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
# chunker = RegexpParser(patterns)
# print("After Regex:",chunker)
# output = chunker.parse(tokens_tag)
# print("After Chunking",output)