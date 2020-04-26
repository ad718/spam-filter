import pandas as pd
df = pd.read_csv('emails.csv')
# display(df.head())

PUNC = [',', '<', '.', '>', '/', '?', ';', ':', "'", '"', '[', ']', '{', '}', '\\', '|',
               '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+' ]

n_spam = len(df[df['spam']==1])
n_ham = len(df[df['spam']==0])


def unique_words(string):
    """Return a set of unique words in the string"""
    for i in PUNC:
        string = string.replace(i, ' ')
    return set(string.split())


def word_count(string):
    """Return a dict {word:count}"""
    
    for i in PUNC:
        string = string.replace(i, ' ')
    word_count = {}
    for w in string.split():
        if w in word_count:
            word_count[w] += 1
        else:
            word_count[w] = 1 
    return word_count

# vocab is a dict with key=word and value=inner_dict,
# inner_dict is a dict with keys:
#     spam_count 
#     ham_count
#     prob_given_spam
#     prob_given_ham 

vocab = {}  

for i, row in df.iterrows():  # index, Series 
    spam = row['spam']  # 0 or 1 
    
    txt = row['text']
    txt = txt.lower() 
    for w in unique_words(txt):
        if w in vocab:
            if spam:
                vocab[w]['spam_count'] += 1
            else:  # ham 
                vocab[w]['ham_count'] += 1
        else: 
            vocab[w] = {}

            if spam:
                vocab[w]['spam_count'] = 1
                vocab[w]['ham_count'] = 0
            else:
                vocab[w]['ham_count'] = 1
                vocab[w]['spam_count'] = 0

# compute probability of each word given spam i.e. P(x|S)
for k in vocab:
    vocab[k]['prob_given_spam'] = (vocab[k]['spam_count'] + 1) / (n_spam + 2)
    vocab[k]['prob_given_ham'] = (vocab[k]['ham_count'] + 1) / (n_ham + 2)
    
print(f"                WORD    PROBABILITY GIVEN SPAM    PROBABILITY GIVEN HAM")
print(f"                ----    ----------------------    ---------------------")
for k,v in vocab.items():
    print(f"{k:>20}    p|S : {v['prob_given_spam']:<13.2}       p|H : {v['prob_given_ham']:<.2}")
          
print('\n\nTRAINING DATA DETAILS')
print('---------------------')
print('n_spam:', n_spam)
print('n_ham :', n_ham)
          
          
def classify(txt):
    """Return ('SPAM'/'HAM', prob_of_being_spam) """
    p_s = n_spam / (n_spam + n_ham)
    p_h = n_ham / (n_spam + n_ham)
    
    txt = txt.lower()
    words = unique_words(txt)
    
    nr = p_s  # numerator
    dr1 = p_s  # first term in denominator
    dr2 = p_h  # second term in denominator

    for word in words:
        if word not in vocab:
            vocab[word] = {}
            vocab[word]['spam_count'] = 1
            vocab[word]['ham_count'] = 1 
            vocab[word]['prob_given_spam'] = 1/(n_spam + 2)
            vocab[word]['prob_given_ham'] = 1/(n_ham + 2)
        
        nr *= vocab[word]['prob_given_spam']
        dr1 *= vocab[word]['prob_given_spam']
        dr2 *= vocab[word]['prob_given_ham']
        
        # prevent from becoming zero
        dr1 = max(5e-324, dr1)
        dr2 = max(5e-324, dr2)
        
    prob_spam_given_txt = nr / (dr1 + dr2)
    return ('SPAM', prob_spam_given_txt) if prob_spam_given_txt > 0.5 else ('HAM', prob_spam_given_txt) 
          
    
def next():
    print(f"\nWant to check another text: [Y/N] ?")
    while True:
        cmd = input()
        if cmd in ['', 'y', 'Y']:
            return True
        elif cmd in ['n', 'N']:
            return False
        else:
            print("\nPlease press either Y or N")
    

def main():
    while True:
        txt = input("\nEnter text you want to check for:")
        result, prob = classify(txt)
        
        print(f"\nThe text you entered is a {result} \nwith spam probability of {prob:.2}")
        if next():
            continue 
        else:
            break 
    return 

if __name__=='__main__':
    main()
