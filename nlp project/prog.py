import nltk, re, os, time, sys
# sys.path.append("file:///home/samhith/this/greenery")

from greenery import fsm


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
    pfile.close()


def processTweet(tweet):
    # process the tweets

    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet
# end


def div(b, c):
    result = -1
    try:
        if c != 0:
            result = float(b) / float(c)
    except:
        print ("invalid input\n")
    return result


# creating database of positive and negative words from a text file
cor = open('Corpus.txt', 'r')
db = dict()
# k=0
for i in cor:
    temp = i.split()
    if len(temp) == 2:
        x = temp[0]
        db[x] = int(temp[1])
cor.close()

# taking input from a file or user
#************************************************************************************
'''
a = input('Enter\n1.To input a file\n2.To input text\n')
a = int(a)
if a == 1:
    # f=str(input('Enter the file name\n'))
    # the file has to be in the same directory or provide the file path
    ffile = open('new.txt', 'r')
if a == 2:
    ffile = open('new.txt', 'w')
    deleteContent(ffile)
    os.system('gedit new.txt')
    # x=input('Press enter if u are done entering the text\nsave the input text file before pressing enter\n')
    ffile = open('new.txt', 'r')
'''
print ""
'''lol=input("Enter the text : ")
lol=lol.split('.')
print lol'''
ffile = open('new.txt', 'r')
fl = ffile.read()
fl=processTweet(fl)
print fl
q = fl.split('.')
ffile.close()
#q=lol
#************************************************************************************
print q
#q1=input("Enter the text : ")
#q=q1.split(' ')
#print q
required_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RS', '-NONE-']
sentence = 0
tot = 0
#print ("***Processing Started***")
# processing the text
for i in range(len(q)):
    #temp = list()
    temp = q[i]
    tokens = nltk.word_tokenize(temp)
    if len(tokens) < 1:
        continue
    if len(tokens) == 1 and (tokens[0] in db):
        ra = db[tokens[0]]
        #print ("word = ", tokens[0])
        #print ("rating = ", ra)
        sentence = sentence + 1

        if ra > 0:
            tot = tot + float(ra / 4)
            # print (tot)
        elif ra == 0:
            continue
        else:
            tot = tot + float(ra / (-4))
            # print (tot)
    if len(tokens) > 1:
        sentence = sentence + 1
        tagged = nltk.pos_tag(tokens)
        # print (tagged)
        tags = list()
        pword = list()
        nword = list()
        l = 0
        flag = 0
        # extracting the required tags and words
        for x in tagged:
            if x[1] in required_tags:
                if x[0] in db:
                    ex = x[0].lower()
                    ra = db[x[0]]

                    #print ("word = ", ex)
                    #print ("rating = ", ra)

                    # categorizing the words as positive,negative or neutral
                    if ra == 0:
                        tags.append('neu')

                    if ra > 0:
                        l = l + 1
                        tags.append('pos')
                        if flag == 1:
                            nword.append((-ra))
                            flag = 0
                        else:
                            pword.append(ra)
                    if ra < 0:
                        l = l + 1
                        tags.append('neg')
                        if flag == 1:
                            pword.append((-ra))
                            flag = 0
                        else:
                            nword.append(ra)

                    if ex == 'not':
                        flag = 1

        #print ("***Processing Ends***")
        # checkink the fsm
        psum = sum(pword)
        nsum = sum(nword)
        tsum = psum + nsum
        pol = 0
        if tsum > 0:
            pol = (float)(tsum / psum)
            if pol != 1:
                pol = pol * 0.5
                tot += pol + 0.5
            else:
                pol = div(max(pword), 4) * 0.5
                tot = tot + pol + 0.5
        elif tsum < 0:
            pol = (float)(tsum / nsum)
            if pol != 1:
                pol = pol * 0.5 * -1
                tot += pol + 0.5
            else:
                pol = div(min(nword), -4) * (-0.5)
                tot = tot + pol + 0.5

if sentence != 0:
    rating = float(tot / sentence) * 100
    print "Rating for the text : ",rating
    if rating <20:
        print "Very Bad"
    elif rating < 40:
        print "Bad"
    elif rating <60:
        print "Neutral"
    elif rating <80:
        print  "Good"
    else:
        print "Very Good"
else:
    print "Error: Sentence zero"
