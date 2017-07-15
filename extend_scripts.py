from nltk import ngrams
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from itertools import chain
from itertools import product
from nltk.corpus import PlaintextCorpusReader
import re


def extend_wordlists(absfile, wordlists, newfolder):

    # create a corpus from abstracts
    corpus = PlaintextCorpusReader('./', absfile)
    # list of new terms
    new = []
    # create a corpus from brown corpus without 'learned' category
    cat = brown.categories()
    cat.pop(brown.categories().index('learned'))
    bc = "".join([" ".join(list_of_words) for list_of_words in
                             brown.sents(categories=cat)])
    # create a bigram set from abstract
    bg = set()
    with open(absfile, "r") as ins:
        for line in ins:
            sentence = line
            sixgrams = ngrams(sentence.lower().split(), 2)
            for grams in sixgrams:
                bg.add(grams)
            #break

    print 'Ngrams done'
    print len(list(bg))

    # for each wordlist
    for txtfile in wordlists:
        with open(txtfile+".txt", "r") as ins:
            linecount = 0
            for line in ins:
                linecount=linecount+1
                if linecount%100==0:
                    print 'Line: '+str(linecount)
                # create bigrams the line in the wordlist
                sentence = line
                bigrams = ngrams(sentence.lower().split(), 2)
                bgl = set()
                for grams in bigrams:
                    bgl.add(grams)
                # if there is just one bigram
                if len(bgl) == 1:
                    gen_list = gen_list(bgl, 0)
                    gen_list.pop(gen_list.index(test))
                    for i in gen_list:
                        if i in bg:
                            if str(i[0]+' '+i[1]).encode('utf-8').strip() not in bc.lower() and i[0]+' '+i[1] not in new:
                                try:
                                    with open('./added3/'+txtfile+'_ext.txt', 'a') as the_file:
                                        #print i[0]+' '+i[1]
                                        new.append(i[0]+' '+i[1])
                                        the_file.write(i[0]+' '+i[1] + '\n')
                                except Exception:
                                    pass
                if len(bgl) >1:
                    y = []
                    ok = True
                    for num in range(len(bgl)):
                        y.append(set())
                        test = list(bgl)[num]
                        lemma1 = set()
                        lemma2 = set()
                        lemma1.add(test[0])
                        lemma2.add(test[1])
                        [lemma1.add(k.name()) for k in chain(
                            *[j.derivationally_related_forms() for j in
                              chain(*[i.lemmas() for i in wn.synsets(test[0])])])]
                        [lemma1.add(k.name()) for k in chain(*[j.pertainyms() for j in
                                                               chain(*[i.lemmas() for i
                                                                       in
                                                                       wn.synsets(
                                                                           test[
                                                                               0])])])]
                        [lemma2.add(k.name()) for k in chain(
                            *[j.derivationally_related_forms() for j in
                              chain(*[i.lemmas() for i in wn.synsets(test[1])])])]
                        [lemma2.add(k.name()) for k in chain(*[j.pertainyms() for j in
                                                               chain(*[i.lemmas() for i
                                                                       in
                                                                       wn.synsets(
                                                                           test[
                                                                               1])])])]
                        gen_list = list(product(lemma1, lemma2))
                        for i in gen_list:
                            if i in bg:
                                y[num].add(i)

                    for num in range(len(bgl)):
                        if len(y[num])==0:
                            ok = False
                        if num>0 and num < (len(bgl)-1):
                            if len(y[num])<len(y[num+1]):
                                ok = False
                        y[num] = list(y[num])

                    if all(i == 1 for i in map(len, y)):
                        ok = False

                    if ok == True:
                        finall = list(product(*y))
                        filtered = []
                        for bgfl in finall:
                            count = {}
                            for eint in bgfl:
                                if eint[0] in count.keys():
                                    count[eint[0]] = count[eint[0]]+1
                                else:
                                    count[eint[0]] = 1
                                if eint[1] in count.keys():
                                    count[eint[1]] = count[eint[1]]+1
                                else:
                                    count[eint[1]] = 1
                            if count.values().count(1)==2:
                                filtered.append(bgfl)
                        if len(filtered) > 1:
                            for v in filtered:
                                text = ''
                                for v2 in v:
                                    if v2[0] in text:
                                        text = text.replace(v2[0], v2[0]+' '+v2[1])
                                    if v2[1] in text:
                                        text = text.replace(v2[1], v2[0]+' '+v2[1])
                                    else:
                                        text = v2[0]+' '+v2[1]
                                if (len(list(ngrams(line.lower().split(), 2))) == len(list(ngrams(text.lower().split(), 2)))) and text.lower().split() != line.lower().split():
                                    myregex = re.compile('\W'+text.encode('utf-8').strip()+'\W')
                                    if len(myregex.findall(corpus.raw().encode('utf-8')))>0 and text.encode('utf-8').strip() not in bc.lower() and text.strip() not in new:
                                        try:
                                            with open('./added3/' + txtfile + '_ext.txt', 'a') as the_file:
                                                print text
                                                new.append(text.strip())
                                                the_file.write(
                                                    text.strip() + '\n')
                                        except Exception:
                                            pass


def gen_vars(bgl, num):
    bg = list(bgl)[num]
    lemma1 = set()
    lemma2 = set()
    lemma1.add(bg[0])
    lemma2.add(bg[1])
    [lemma1.add(k.name()) for k in chain(
        *[j.derivationally_related_forms() for j in
          chain(*[i.lemmas() for i in wn.synsets(bg[0])])])]
    [lemma1.add(k.name()) for k in chain(*[j.pertainyms() for j in
                                           chain(*[i.lemmas() for i in
                                                   wn.synsets(
                                                       bg[0])])])]
    [lemma2.add(k.name()) for k in chain(
        *[j.derivationally_related_forms() for j in
          chain(*[i.lemmas() for i in wn.synsets(bg[1])])])]
    [lemma2.add(k.name()) for k in chain(*[j.pertainyms() for j in
                                           chain(*[i.lemmas() for i in
                                                   wn.synsets(
                                                       bg[1])])])]
    return list(product(lemma1, lemma2))



extend_wordlists('abstract.txt', ['cno','brain','cel','dis','func','inv','mol','NMOBR','brain_nn'], './added5/')
