
def formatQuestion(quest, answers, answer): #quest:description of the question, answers: string containing answers, answer:string containing the answer letter e.g. "D"
    return '''
<question type="multichoice">
    <name>
        <text>{}</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[{}]]></text>
    </questiontext>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>none</answernumbering>
    {}
</question>
'''.format(quest.split('\n')[0], '&nbsp;'.join('&emsp;'.join('<br>'.join(quest.split('\n')).split('\t')).split(' ')), answers)[1:] #remove first \n
#asd
#will run on every answer, answer:answer text, isCorrect: is this the correct answer
def formatAnswer(answer, isCorrect):    #answer
    if isCorrect:
        a = '100'
    else:
        a = '0'
    return '''
    <answer fraction="{}">
        <text>{}</text>
    </answer>'''.format(a, answer)[1:]
#asd


def save(filename, l):
    x = open(filename, mode='w', encoding='utf-8')
    x.write('''<?xml version="1.0" ?>
<quiz>
{}
</quiz>'''.format(''.join(l)))
    x.close()
    


def isNumber(c):
    return(c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9')

def isNumEnd(text, i):
    return(text[i] == '.' and (text[i+1] == '\t' or text[i+1] == ' '))

def isNewQuestion(text, i, q):
    if (text[i] == '\n' and i+4 < len(text)):
        try:
            if(q < 10):
                if(int(text[i+1]) == q and isNumEnd(text, i+2)):
                    return(4)
            else:
                if(int(text[i+1:i+3]) == q and isNumEnd(text, i+3)):
                    return(5)
        except:
            return(0)
        return(0)

def isAnswerLetter(l):
    return(l == 'A' or l == 'B' or l == 'C' or l == 'D')

#def isAnswerNext(item, i):
    
class AnswerLetterCounter:
    def __init__(self):
        self.letter = "D"

    def next(self):
        if (self.letter == "D"):
            self.letter = 'C'
            return(True)
        elif (self.letter == 'C'):
            self.letter = 'B'
            return(True)
        elif (self.letter == 'B'):
            self.letter = 'A'
            return(True)
        else:
            return(False)

    def __str__(self):
        return('({})'.format(self.letter))
    def get(self):
        return(self.letter)

    def isAnswer(self, item, i):
        if(item[i-3: i] == str(self)):
            #print(item[i])
            i -= 4
            while (item[i] == ' ' or item[i] == '\t'):
               i -= 1
            return(item[i] == '\n')
        return(False)


def processItem(item):
    i = len(item)-1
    answer = 'X'
    while(i != 0 and not isAnswerLetter(item[i])):
        i -= 1
    if (isAnswerLetter(item[i])):
        answer = item[i]
        i -= 1

    answerLetter = AnswerLetterCounter()
    
    answers = []
    
    while True:
        while(item[i] == ' ' or item[i] == '\n' or item[i] == '\t'):
            #print('debug: ' + item[i])
            i -= 1
            
        answerEnd = i + 1
        
        while not(answerLetter.isAnswer(item, i)):
            if item[i] == '\n':
                item = '{} {}'.format(item[:i], item[i+1])
            i -= 1
        if answerLetter.get() == "X":
            print('WARNING, cannot find correct answer:\n{}'.format(item))
        answers = [formatAnswer(item[i+1:answerEnd], answerLetter.get() == answer)] + answers   
        #answers = ['{}. {}'.format(answerLetter.get(), item[i+1:answerEnd])] + answers
        i -= 4
        if not answerLetter.next():
            break

    while (item[i] == ' ' or item[i] == '\t' or item[i] == '\n'):
        i -= 1

    
    return(formatQuestion(item[:i+1], '\n'.join(answers), answer))
    #return('{}\n\n{}\nANSWER: {}'.format(item[:i+1], '\n'.join(answers), answer))


def process(text):
    text = '\n' + text
    while text[1] == '\n':
        text = text[1:]
    l = []
    currentItem = ''
    step = 0
    q = 1
    while step < len(text):
        if(bool(isNewQuestion(text, step, q))):
            if (len(currentItem) != 0):
                l = l + [processItem(currentItem)]
            currentItem = ''
            step += isNewQuestion(text, step, q)
            q += 1
        else:
            currentItem = currentItem + text[step]
            step += 1
    l = l + [processItem(currentItem)]
    return l

def printl():   #just a debug method
    print('\n--------------------------------\n'.join(l))

def openfile(filename):
    x = open(filename ,mode = "r", encoding = 'utf-8')

    text = x.read()
    x.close()
    return text

if __name__ == "__main__":
    sc = True
    while sc:
        try:
            x = open(input("UTF-8 encoded file name with extension e.g. quests.txt\n"), mode = 'r', encoding = 'utf-8')
            t = x.read()
            x.close()
            sc = False
        except:
            print('wrong filename or encoding')
    l = process(t)
    sc = True
    while sc:
        try:
            save(input('export file name e.g. quests.xml\nWARNING, this file will be owerwrited\n'), l)
            sc = False
        except:
            print('unexcepted error')


