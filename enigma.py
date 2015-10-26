
ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Rotor:
    def __init__(self, number):
        self.offsets_new=[[4, 9, 10, 2, 7, 1, -3, 9, 13, 16, 3, 8, 2, 9, 10, -8, 7, 3, 0, -4, -20, -13, -21, -6, -22, -16],
                      [0, 8, 1, 7, 14, 3, 11, 13, 15, -8, 1, -4, 10, 6, -2, -13, 0, -11, 7, -6, -5, 3, -17, -2, -10, -21],
                      [1, 2, 3, 4, 5, 6, -4, 8, 9, 10, 13, 10, 13, 0, 10, -11, -8, 5, -12, -19, -10, -9, -2, -5, -8, -11],
                      [4, 17, 12, 18, 11, 20, 3, -7, 16, 7, 10, -3, 5, -6, 9, -4, -3, -12, 1, -13, -10, -18, -20, -11, -2, -24],
                      [21, 24, -1, 14, 2, 3, 13, 17, 12, 6, 8, -8, 1, -6, -3, 8, -16, 5, -6, -10, -4, -7, -17, -19, -22, -15]]
        self.triggers=[ALPHABET.index('R'), ALPHABET.index('F'), ALPHABET.index('W'), ALPHABET.index('K'), ALPHABET.index('A')]
        self.ALPHABET=ALPHABET
        self.number=number
        self.offset=[self.offsets_new[number-1],[]]
        for i in range(26):
            for k in range(26):
                if (k+self.offset[0][k])%26==i:
                    self.offset[1].append(-self.offset[0][k])
                    break
        self.start_pos=self.offset[:]
        self.trigger=0

    #rotation of ring leads to new offsets configuration
    def rotate_ring(self,*, up):
        if up:
            self.offsets=list((self.offsets[-1],))+self.offsets[0:-1]
        else:
            self.offsets=self.offsets[1:]+list((self.offsets[0],))
        self.substitution=self.construct_sub()

    #set rotors to start position
    def initialization(self, rings_combination, rotors_start):
        self.offset=self.start_pos[:]
        offset=(ALPHABET.index(rotors_start)-ALPHABET.index(rings_combination))%26
        self.offset[0]=self.offset[0][offset:]+self.offset[0][:offset]
        self.offset[1]=self.offset[1][offset:]+self.offset[1][:offset]
        self.trigger=ALPHABET.index(rotors_start)


    #rotation of rotor change positions of input and output signs
    def rotate(self, *, up):
        if up:
            self.offset[0]=self.offset[0][1:]+list([self.offset[0][0]])
            self.offset[1]=self.offset[1][1:]+list([self.offset[1][0]])
            self.trigger=(self.trigger+1)%26
        else:
            self.offset[0]=self.offset[0][1:]+list([self.offset[0][0]])
            self.offset[1]=self.offset[1][1:]+list([self.offset[1][0]])
            self.trigger=(self.trigger+1)%26
        if self.trigger==self.triggers[self.number-1]:
            return True
        else:
            return False

    def encipher(self, ch):
        return (ch+self.offset[0][ch])%26

    def decipher(self, ch):
        return (ch+self.offset[1][ch])%26

class Reflector:
    def __init__(self, type):
        if type=='B':
            self.substitution=[24, 16, 18, 4, 12, 13, 5, -4, 7, 14, 3, -5, 2, -3, -2, -7, -12, -16, -13, 6, -18, 1, -1, -14, -24, -6]
        elif type=='C':
            self.substitution=[5, 20, 13, 6, 4, -5, 8, 17, -4, -6, 7, 14, 11, 9, -8, -13, 3, -7, 2, -3, -2, -20, -9, -11, -17, -14]
        elif type=='A':
            self.substitution=[4, 8, 10, 22, -4, 6, 18, 16, 13, -8, 12, -6, -10, 4, 2, 5, -2, -4, 1, -1, -5, -13, -12, -16, -18, -22]

    def reflection(self, ch):
        return ch + self.substitution[ch]

class Plugboard:
    def __init__(self, pairs):
        self.alphabet=[list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
        lst=list(self.alphabet[1])
        for i in range(len(self.alphabet[1])):
            if self.alphabet[1][i] in pairs.keys():
                index=self.alphabet[1].index(pairs[self.alphabet[1][i]])
                lst[i], lst[index] = lst[index], lst[i]
        self.alphabet[1]=''.join(lst)

class Enigma:
    def __init__(self, *, rotors, reflector, plugboard):
        self.alphabet=ALPHABET
        self.rotors=[Rotor(i) for i in rotors]
        self.reflector=Reflector(reflector)
        self.plugboard=plugboard

    #set Enigma's rotors to start position
    def initialization2(self, rings_combination, rotors_start, rotors=None):
        if rotors:
            self.rotors=[Rotor(i) for i in rotors]
        self.rings_combinations=rings_combination
        self.rotors_start=rotors_start
        for i in range(len(self.rotors)):
            self.rotors[i].initialization(rings_combination[i], rotors_start[i])


    #encrypt selected character
    def encryption(self, letter, IsRotatable):
        ch=self.plugboard.alphabet[0].index(letter)
        ch=self.plugboard_stage(ch, forward=True)
        ch=self.rotors_stage(True, ch, IsRotatable)
        ch=self.reflector.reflection(ch)
        ch=self.rotors_stage(False, ch, IsRotatable)
        ch=self.plugboard_stage(ch, forward=False)
        return ALPHABET[ch]


    def plugboard_stage(self, ch, forward):
        if forward:
            ch1=self.plugboard.alphabet[1][ch]
            return self.plugboard.alphabet[0].index(ch1)
        else:
            ch1=self.plugboard.alphabet[0][ch]
            return self.plugboard.alphabet[1].index(ch1)

    #rotor stage. Before encryption right rotor should to be rotated
    def rotors_stage(self, forward, ch, IsRotatable):
        if forward:
            move_next=False
            for i in range(2,-1,-1):
                if (i==2  or move_next) and IsRotatable:
                    move_next=self.rotors[i].rotate(up=True)
                ch=self.rotors[i].encipher(ch)
        else:
            for i in range(3):
                ch=self.rotors[i].decipher(ch)

        return ch

    #set rotors to specific position, using for cryptanalysis only
    def set_rotors_step(self, rings_combination, rotors_start, rotors, step):
        self.initialization2(rings_combination, rotors_start)
        move_next=False
        for i in range(2,-1,-1):
            for k in range(step):
                if (i==2):
                    move_next=self.rotors[i].rotate(up=True)
                if (move_next):
                    move_next=self.rotors[i-1].rotate(up=True)


#test message from this page http://www.codesandciphers.org.uk/enigma/emachines/enigmad.htm
def _enigmatest():
    plug=Plugboard({'D':'N', 'G':'R', 'I':'S', 'K':'C', 'Q':'X', 'T':'M', 'P':'V', 'H':'Y', 'F':'W', 'B':'J'})
    myenigma=Enigma(rotors=[4, 2, 5], reflector="B", plugboard=plug)
    myenigma.initialization2('GMY', 'RLP')
    test='NQVLT YQFSE WWGJZ GQHVS EIXIM YKCNW IEBMB ATPPZ TDVCU PKAY'
    text=''
    for ch in test:
        if ch!=' ':
            text+=myenigma.encryption(ch, True)
    print(text)
    expected='FLUGZEUGFUEHRERISTOFWYYXFUELLGRAFXFUELLGPAFXPOFOP'
    if text==expected:
        print("Correct")


