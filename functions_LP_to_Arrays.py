import sys
import re
import pandas as pd
import numpy as np

# Μέθοδος η οποία ελέγχει αν η λιστα newList που προέρχεται απο το αρχειο text
# έχει την κατάλληλη διαμόρφωση 
def checkFormation(newList):

    # Ψάχνει όλα τα στοιχεία της λίστας όπως ήταν χωρισμένα σε γραμμές στο αρχικό αρχείο
    for i in range(len(newList)):
        
        # Μεταβλητή τύπου boolean που θα βοηθήσει να βρεθεί η ύπαρξη λάθους
        # και στην διακοπή του προγράμματος
        flag = True
        
        if i==0:
            
            # Έλεγχος για την ύπαρξη min ή max στην πρώτη γραμμή του αρχείου
            for minmax in ['min', 'max']:
                if minmax in newList[i]:
                    flag = False
                    
            if flag == False:
                minmax_text = 'The word min OR max exists'
            else:
                minmax_text = 'The word min OR max doesnt exist'
                
            # Βρίσκει στην πρώτη γραμμή που υπάρχει το σύμβολο = ώστε να ψάξει
            # το πλήθος των x απο εκει και έπειτα
            # Γινεται για την αποφυγή του γράμματος x απο την λέξη max
            pos_of_equal_symbol = re.search('=', newList[i])
            pos_of_first_x_after_equal_symbol = re.search('x', newList[i][pos_of_equal_symbol.end():])
            
            # Έτσι η ΄θεση του πρώτου x για το συνολικό μήκος του string newList
            # είναι το άθροισμα της θέσης του = (μεσα στο newList[0])
            # και της θέσης του πρώτου x (απο το = μέχρι το τελος του string newList[0])
            # Άρα το pos_of_first_x έχει την πρώτη θέση του x στην πρώτη γραμμή
            pos_of_first_x = pos_of_equal_symbol.end() + pos_of_first_x_after_equal_symbol.start()
                
            # Βρίσκει το πλήθος των x
            count_of_x = len(re.findall('x', newList[i][pos_of_first_x:]))
                
            # Βρίσκει το πλήθος των - και +
            count_of_plus_minus=0
            for symbol in '+-':
                count_of_plus_minus += newList[i][pos_of_first_x:].count(symbol)
            
            # Εάν το πλήθος των - και + είναι κατά 1 μικρότερο απο το πλήθος 
            # των x σημαίνει οτι δεν λείπει κανένα - ή +
            # Αυτό συμβαίνει γιατί ψάχνει το πλήθος των x χω΄ρίς το πρόσημο
            # του πρώτου x
            # Και αν υπάρχει η λέξη min ή max (μέσω του flag)
            # Εμφανίζει τα αντιστοιχα μηνύματα στην κονσόλα ή
            # Διακόπτει το πρόγραμμα
            if count_of_plus_minus == count_of_x - 1 and flag == False:
                print('First line is correct')
                print(minmax_text, 'and plus OR minus symbols are correct')
            else:
                print('There is a problem in the first line')
                print(minmax_text, 'and plus OR minus symbols are NOT correct')
                sys.exit(1)
            
        elif i==1:
            
            # Έλεγχος για την ύπαρξη st ή s.t. ή subjectto (λόγω της αφαίρεσης των κενών)
            # στην δεύτερη γραμμή του αρχείου 
            for st in ['st', 's.t.', 'subjectto']:
                if st in newList[i]:
                    flag = False
            
            if flag == False:
                print('Line ', i+1,'is correct')
            else:
                print('There is a problem in ', i+1,'line')
                sys.exit(1)
        
        # Το range είναι απο την τρίτη γραμμή του περιορισμού μέχρι την
        # προτελευταία γραμμή δηλαδή χωρίς το end
        elif i in range(2,len(newList)-1):
        
            # Έλεγχος ύπαρξης του = σε κάθε γραμμή του περιορισμού 
            # (Αφού πρέπει να υπάρχει <= ή = ή >=, οπότε τα περιλαμβάνει το =)
            # Αν βρεθεί ψαχνει για την ύπαρξη αριθμού μετά απο το = 
            number = '-?\d+\.?\d*'

            if '=' in newList[i]:
                equal_symbol_text = 'The = symbol exists'
            
                pos_of_equal_symbol = re.search('=', newList[i])
            
                if len(re.findall(number, newList[i][pos_of_equal_symbol.end():])):
                    b_text = 'The b[',i+1,'] exists'
                else:
                    b_text = 'The b[',i+1,'] doesnt exist'
                    flag = False
            else:
                equal_symbol_text = 'The = symbol doesnt exists in line ' + i+1
                print(equal_symbol_text)
                sys.exit(1)
        
            # Χρησιμοποιείται η ίδια λογική που υπάρχει και στην πρώτη γραμμή
            # με την διαφορά ότι ψαχνει απο το πρώτο x μέχρι το =
            pos_of_first_x = re.search('x', newList[i])
            pos_of_equal_symbol = re.search('=', newList[i])
        
            count_of_x = len(re.findall('x', newList[i][pos_of_first_x.start():pos_of_equal_symbol.start()]))
        
            count_of_plus_minus=0
            for symbol in '+-':
                count_of_plus_minus += newList[i][pos_of_first_x.start():pos_of_equal_symbol.start()].count(symbol)
        
        
            if count_of_plus_minus == count_of_x - 1 and flag:
                print('Line ', i+1,'is correct')
                print(equal_symbol_text, 'and', b_text)
            else:
                print('There is a problem in ', i+1,'line')
                print(equal_symbol_text, 'and', b_text)
                sys.exit(1)

# Μέθοδος η οποία βρίσκει τις διαστάσεις που θα έχουν οι πίνακες     
def calculateDimensions(aList):
    
    # Αν υπάρχει η λέξη max θα εντοπιστεί και το x απο το max 
    # παραγμα το οποίο είναι ανεπιθύμητο για μας και γαι αυτο
    # υπάρχει το n-cn στο return
    cn=0
    if 'max' in aList[0]:
        cn += 1
        
    m = n = 0
    for i in aList[0]:
        if 'x' in i and not(i=='max'):
            n += 1       
    print('n value is:', n)
    
    # Το m βρίσκει πόσοι είναι οι τεχνολογικοί περιορισμοί εφόσον
    # γνωρίζουμε ότι βρίσκεται ανάμεσα στο st και το end
    for i in aList[2:-1]:
        m += 1
    print('m value is:', m)
    
    return m, n-cn

def getMinMax(aList):
    # Βρίσκει την τιμή του minMax εφόσον πιο πριν έχουμε ελέγξει 
    # για την ύπαρξει του min ή max
    if 'min' in aList[0]:
        return -1
    elif 'max' in aList[0]:
        return 1
    
def add_One_or_minusOne(newList):
    
    # Ψάχνει όλα τα στοιχεία της λίστας όπως ήταν χωρισμένα σε γραμμές στο αρχικό αρχείο
    for i in range(len(newList)):
        pos_of_x = []
        if i==0:
        
            # Η ίδια λογική της πρώτης γραμμής με την μέθοδο checkFormation(newList)
            pos_of_equal_symbol = re.search('=', newList[i])
            pos_of_first_x_after_equal_symbol = re.search('x', newList[i][pos_of_equal_symbol.end():])
            pos_of_first_x = pos_of_equal_symbol.end() + pos_of_first_x_after_equal_symbol.start()
            
            #Βρίσκει τις θέσεις των x (το ξεκίνημα τους) και εισάγωνται σε μία λίστα pos_of_x
            match = re.finditer('x', newList[i][pos_of_equal_symbol.end():])
            for ma in match:
                #print (pos_of_equal_symbol.end()+ma.start())
                pos_of_x.append((pos_of_equal_symbol.end()+ma.start()))
            
            # Γίνονται οι έλεγχοι έαν η θέση πριν από το x αποτελείται απο 
            # κάτι διαφορετικό απο νούμερο ή - ή + και προστίθεται σε εκείνη 
            # την θέση 1 ή -1
            # Επειδή προστίθονται char χαρακτήρες 1 ή 2 αλλάζουν και οι θέσεις
            # των επόμενων x, οπότε προστίθονται 1 ή 2 στις θέσεις των επόμενων
            # x ωστέ να παραμείνουν σωστές και οι θέσεις των x
            for x in pos_of_x:
                if not(newList[i][x-1].isdigit()) or newList[i][x-1] == '-' or newList[i][x-1] == '+':
                    if newList[i][x-1] == '-':
                        newList[i] = newList[i][0:x] + str(-1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 2
                    else:
                        newList[i] = newList[i][0:x] + str(1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 1
                        
        elif i in range(2,len(newList)-1):
            
            # Επικρατεί η ίδια λογική με την διαφορά ότι δεν υπάρχει η λέξη max
            # για να με μπερδέψει το x απο το max
            match = re.finditer('x', newList[i])
            for ma in match:
                #print (m.start())
                pos_of_x.append(ma.start())
            
            for x in pos_of_x:
                if not(newList[i][x-1].isdigit()) or newList[i][x-1] == '-' or newList[i][x-1] == '+' or x == 0:
                    if newList[i][x-1] == '-':
                        newList[i] = newList[i][0:x] + str(-1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 2
                    else:
                        newList[i] = newList[i][0:x] + str(1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 1
                            
def insertIntoTables(newList, m, n):
    
    # Δημιουργεί τους πίνακες τύπου DataFrame που θα φυλοξενήσουν τα αποτελέσματα
    A = pd.DataFrame(index = np.arange(m), columns = np.arange(n))
    b = pd.DataFrame(index = np.arange(m), columns = np.arange(1))
    c = pd.DataFrame(index = np.arange(1), columns = np.arange(n))
    Eqin = pd.DataFrame(index = np.arange(m), columns = np.arange(1))

    # Το μοτίβο για να βρεθεί ο αριθμός πριν απο το x
    num_b4_x = r"(-?\d+\.?\d*)x"
    # Το μοτίβο για να βρεθεί ο αριθμός μετά απο το x
    num_after_x = r"x(-?\d+\.?\d*)"

    for i in range(len(newList)):
        if i==0:
            
            # Βρίσκονται οι αριθμοί πριν απο το x και μετα απο το x αντίστοιχα
            num_x = re.findall(num_b4_x, newList[i])
            x_num = re.findall(num_after_x, newList[i])
            
            # Εισάγωνται στον πίνακα c οι αριθμοί πριν απο το x (num_x)
            # για γραμμές i και στήλες j (x_num)
            for j in range(len(x_num)):
                c.iloc[i,int(x_num[j])-1] = int(num_x[j])
                
        elif i in range(2,len(newList)-1):
            
            # Η ίδια λογική με πιο πανω μόνο που τωρα εισάγωνται στον πίνακα A
            num_x = re.findall(num_b4_x, newList[i])
            x_num = re.findall(num_after_x, newList[i])
            
            for j in range(len(x_num)):
                A.iloc[i-2,int(x_num[j]) -1] = int(num_x[j])
    
    # Στα στοιχεία που δεν εχουν τιμή εισάγεται η τιμή 0
    A = A.fillna(0)        
    
    # Το μοτίβο για να βρεθεί ο αριθμός μετά απο το =
    num_after_equal_sym = r"=(-?\d+\.?\d*)"

    # Εισάγεται στον πίνακα b οι τιμές μετά το = μέσω του μοτίβου
    for i in range(len(newList[2:-1])):
        b.loc[i,0] = int(re.findall(num_after_equal_sym, newList[2:-1][i])[0])
        
        # Βρίσκεται εάν σε κάθε γραμμή των περιορισμών υπάρχει <= ή = ή >=
        # και προστίθονται οι αντίστοιχες τιμές στον πίνακα Eqin
        if '<=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = -1
        elif '>=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = 1
        elif '=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = 0
            
    return A, b, c, Eqin