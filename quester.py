x = open("quests.txt",mode = "r", encoding = 'utf-8')

text = x.read()
x.close()


def formatQuestion(quest, answers, answer):
    return '''
<question type="multichoice">
    <name>
        <text>{}</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[{}]]></text>
    </questiontext>
    <answernumbering>none</answernumbering>
    {}
</question>
'''.format(quest.split('\n')[0], '&emsp;'.join('<br>'.join(quest.split('\n')).split('\t')), answers)[1:] #remove first \n
#asd

def formatAnswer(answer, isCorrect):
    if isCorrect:
        a = '100'
    else:
        a = '0'
    return '''
    <answer fraction="{}">
        <text>{}</text>
    </answer>'''.format(a, answer)[1:]
#asd



l = []
currentItem = ''

step = 0
q = 1
def isNumber(c):
    return(c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9')

def isNumEnd(i):
    return(text[i] == '.' and (text[i+1] == '\t' or text[i+1] == ' '))

def isNewQuestion(i):
    if (text[i] == '\n' and i+4 < len(text)):
        try:
            if(q < 10):
                if(int(text[i+1]) == q and isNumEnd(i+2)):
                    return(4)
            else:
                if(int(text[i+1:i+3]) == q and isNumEnd(i+3)):
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
        answers = [formatAnswer(item[i+1:answerEnd], answerLetter.get() == answer)] + answers   
        #answers = ['{}. {}'.format(answerLetter.get(), item[i+1:answerEnd])] + answers
        i -= 4
        if not answerLetter.next():
            break

    while (item[i] == ' ' or item[i] == '\t' or item[i] == '\n'):
        i -= 1

    
    return(formatQuestion(item[:i+1], '\n'.join(answers), answer))
    #return('{}\n\n{}\nANSWER: {}'.format(item[:i+1], '\n'.join(answers), answer))


while step < len(text):
    if(bool(isNewQuestion(step))):
        if (len(currentItem) != 0):
            l = l + [processItem(currentItem)]
        currentItem = ''
        step += isNewQuestion(step)
        q += 1
    else:
        currentItem = currentItem + text[step]
        step += 1
l = l + [processItem(currentItem)]

def printl():   #just a debug method
    print('\n--------------------------------\n'.join(l))

def save(filename):
    x = open(filename, mode='w', encoding='utf-8')
    x.write('''<?xml version="1.0" ?>
<quiz>
{}
</quiz>'''.format(''.join(l)))
    x.close()
    
