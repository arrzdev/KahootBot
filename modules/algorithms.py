'''
    PHRASE COMPARATION ALGORITHM
    DATE: 25/02/2020
    AUTHOR: ARRZ.DEV
'''

#ALGO TO FIND THE CLOSEST ONE
def identify_question(dictionary=False, question=False):
    if not dictionary or not question:
        return 'missing parameter'
        
    #define vars
    phraseBest = ''
    probBest = 0

    #create the correct words dictionary
    questionWords = question.split(' ')

    for attemp in dictionary:

        #NORMALIZE ATTEMP
        ###

        #create attemp words dictionary
        attempWords = attemp.split(' ')

        #check if the amount of words is less or equal than 1/3 of the original one and skip it in that case
        if len(attempWords) <= (len(questionWords)/3):
            continue  

        #init probability as 0
        prob = 0


        for word_index in range(len(questionWords)):
            try:
                #print(f'W: {attempWords[word_index]}')
                if attempWords[word_index] == questionWords[word_index]:
                    prob += (5/(5*len(questionWords)))*100
                else:
                    #if the word isnt 100% equal divide in letters and test it!
                    #create both attemp and correct letter dictionary

                    #loop trough letters
                    for letter_index in range(len(questionWords[word_index])):

                        #print(f'L: {questionWords[word_index][letter_index]}')

                        if attempWords[word_index][letter_index] == questionWords[word_index][letter_index]:
                            prob += ((5/len(questionWords[word_index]))/(5*len(questionWords)))*100
                        else:
                            #add the penalty here for each letter
                            pass

            except:
                pass

        #check if it a better option
        if prob > probBest:
            probBest = prob
            phraseBest = attemp
           
        #print if prob is != 0%
        #if prob != 0:
            #print(f'  MATH.PROB: {prob}')

        #kill switch in case probability is already 100%
        if prob > 99.9:
            break

    return probBest, phraseBest

def identify_answer_index(answer=False, dictionary=False):
    if not dictionary or not answer:
        return 'missing parameter'

    if len(dictionary[::]) > 3:
        #define vars
        answerBest = ''
        probBest = 0

        #create the correct words dictionary
        answerWords = answer.split(' ')

        for attemp in dictionary:

            #NORMALIZE ATTEMP
            ###

            #create attemp words dictionary
            attempWords = attemp.split(' ')

            #check if the amount of words is less or equal than 1/3 of the original one and skip it in that case
            if len(attempWords) <= (len(answerWords)/4):
                continue  

            #init probability as 0
            prob = 0


            for word_index in range(len(answerWords)):
                try:
                    #print(f'W: {attempWords[word_index]}')
                    if attempWords[word_index] == answerWords[word_index]:
                        prob += (5/(5*len(answerWords)))*100
                    else:
                        #if the word isnt 100% equal divide in letters and test it!
                        #create both attemp and correct letter dictionary

                        #loop trough letters
                        for letter_index in range(len(answerWords[word_index])):

                            #print(f'L: {questionWords[word_index][letter_index]}')

                            if attempWords[word_index][letter_index] == answerWords[word_index][letter_index]:
                                prob += ((5/len(answerWords[word_index]))/(5*len(answerWords)))*100
                            else:
                                #add the penalty here for each letter
                                pass

                except:
                    pass

            #check if it a better option
            if prob > probBest:
                probBest = prob
                answerBest = attemp
                
            #print if prob is != 0%
            #if prob != 0:
                #print(f'  MATH.PROB: {prob}')

        try:
            return probBest, dictionary.index(answerBest)
        except:
            return False
    else:
        return False

#FIRST ALGORITHM ATTEMP
'''
    temp_seed = 0
    for i in k:
        if i.isalpha():
            temp_seed += ord(i)
        
        elif i.isnumeric():
            temp_seed += int(i)
            
    if temp_seed > question_seed:
        probability = question_seed/temp_seed
            
    else:
        probability = temp_seed/question_seed

    if probability > 0.65 and probability > best:
        best = probability
        best_question = k


    return best, best_question
'''