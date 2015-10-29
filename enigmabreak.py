import enigma
import datetime
import multiprocessing
ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

test='GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ'
text='FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT'


#print possible cycles. Is chain begins and ends with one character it is cycle
#For example: N->K->T->N; N->T; N->A->L->R->N; N->A->O->S->N
def searchCycles(a, b, num):
    tmp1=a[num]
    tmp2=b[num]
    a=a[:num]+list('0')+a[num+1:]
    b=b[:num]+list('0')+b[num+1:]
    print(num, tmp1, tmp2)
    IsFound=True
    while IsFound:
        for i in range(len(a)):
            IsFound=False
            if a[i]==tmp2 and a[i]!='0':
                tmp1=a[i]
                tmp2=b[i]
                a=a[:i]+list('0')+a[i+1:]
                b=b[:i]+list('0')+b[i+1:]
                print(i, tmp1, tmp2)
                IsFound=True
                break



for i in range(len(test)):
    searchCycles(list(test), list(text), i)
    print('-----------')
print('--------')

#This function works only for specific plaintext, if you want to decrypt another message you should to rewrite this method
# Searching rotors start positions with selected cycles:
#71.N-14.K-37.T-N; 32.N-10.T-N; 39.N-5.A-16.L-13.R-N; 32.N-10.T-N-37.T-N; 34.N-22.A-48.O-3.S-N
def globalSearch(start, end):
    plug=enigma.Plugboard({})
    myenigmas=[]
    for i in range(15):
        myenigmas.append(enigma.Enigma(rotors=[2, 1, 3], reflector="A", plugboard=plug))
        myenigmas[i].initialization2('AAA', 'AAA')
    offsets=[72, 15, 38, 33, 11, 40, 6, 17, 14, 11, 38, 40, 23, 49, 4]
    found=False
    for a in range(start, end):
        if found:
                    break
        for b in range(len(ALPHABET)):
            if found:
                    break
            for c in range(len(ALPHABET)):
                if found:
                    break
                for d in range(len(ALPHABET)):
                    for i in range(15):
                        myenigmas[i].set_rotors_step(ALPHABET[a]+ALPHABET[b]+ALPHABET[c], 'AA'+ALPHABET[d], [2, 1, 3], offsets[i])

                    for i in range(len(ALPHABET)):
                        #test cycle
                        text1=myenigmas[0].encryption(ALPHABET[i], False)
                        text1=myenigmas[1].encryption(text1, False)
                        text1=myenigmas[2].encryption(text1, False)

                        # and another one
                        text2=myenigmas[3].encryption(ALPHABET[i], False)
                        text2=myenigmas[4].encryption(text2, False)

                        #and another
                        text3=myenigmas[5].encryption(ALPHABET[i], False)
                        text3=myenigmas[6].encryption(text3, False)
                        text3=myenigmas[7].encryption(text3, False)
                        text3=myenigmas[8].encryption(text3, False)

                        #one more cycle
                        text4=myenigmas[9].encryption(ALPHABET[i], False)
                        text4=myenigmas[10].encryption(text4, False)

                        #last one
                        text5=myenigmas[11].encryption(ALPHABET[i], False)
                        text5=myenigmas[12].encryption(text5, False)
                        text5=myenigmas[13].encryption(text5, False)
                        text5=myenigmas[14].encryption(text5, False)
                        if ALPHABET[i]==text1 and ALPHABET[i]==text2 and ALPHABET[i]==text3 and ALPHABET[i]==text4 and ALPHABET[i]==text5:
                            found=True
                            print('N connected to '+ALPHABET[i]+' on plugboard')
                            print('Rotors positions: %s%s%s' %(ALPHABET[a],ALPHABET[b],ALPHABET[c]))
                            print('Rings positions: AA%s' %ALPHABET[d])
                            print(datetime.datetime.now())

    print("End: "+str(datetime.datetime.now()))

print("Working on it...")
print("Start: "+str(datetime.datetime.now()))

if __name__=="__main__":
    p1 = multiprocessing.Process(target=globalSearch, args=(0, 6))
    p2 = multiprocessing.Process(target=globalSearch, args=(6, 13))
    p3 = multiprocessing.Process(target=globalSearch, args=(13, 20))
    p4 = multiprocessing.Process(target=globalSearch, args=(20, 26))

    p1.start()
    p2.start()
    p3.start()
    p4.start()