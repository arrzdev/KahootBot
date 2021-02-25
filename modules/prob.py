'''
    PHRASE COMPARATION ALGORITHM
    DATE: 25/02/2020
    AUTHOR: ARRZ.DEV
'''

def calc_prob(dictionary=False, question=False): 
    if not dictionary or not question:
        return 'argument missing' 

    best_question = ''
    fitness = 0

    #DIVIDE
    question_words = question.split(' ')

    #ITERATE TROUGH THE DICTIONARY
    for db_question in dictionary:
        db_question_words = db_question.split(' ')
        temp_fitness = 0
        for word in db_question_words:
            try:
                if word == question_words[db_question_words.index(word)]:
                    temp_fitness += 5
            except:
                pass
        
        if temp_fitness > fitness:
            fitness = temp_fitness
            best_question = db_question

    best_prob = fitness/(len(question_words)*5)

    #ROUND TO 100%
    if best_prob > 1:
        best_prob == 1

    return best_prob, best_question






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