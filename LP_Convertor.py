# Εισάγω τις μεθόδους απο το αρχείο functions_Ex01LP.py
from functions_LP_to_Arrays import *

# Open a file
try:
    file = open('LP-1.txt', 'r');
except IOError:
    print("The file you wanted to open, it doesn't exist..")
    exit (1)

# Reads the file in lines
f = file.readlines();

# Close opened file
file.close()

# Δημιουργία κενής λίστας
newList = []

# Εισάγω την λίστα f στην λίστα newList χωρίς τους χαρακτήρες , και \n 
# και ώστε να την διαχειριστώ πιο εύκολα
for line in f:
    
# Ελέγχει αν υπάρχει κενη γραμμή για να την προσπεράσει
    if (line.isspace()):
        continue
    else:
        newList.append(line.strip(',\n'))

# Αφαιρώ τα κενά απο την λίστα
newList = [line.replace(' ', '') for line in newList]

# Μέθοδος η οποία ελέγχει αν η λιστα newList που προέρχεται απο το αρχειο text
# έχει την κατάλληλη διαμόρφωση 
checkFormation(newList)

# Μέθοδος η οποία βρίσκει τις διαστάσεις που θα έχουν οι πίνακες
m, n = calculateDimensions(newList)

# Μέθοδος η οποία εισάγει 1 ή -1 μπροσ΄τα απο το x με τις ανάλογες συνθήκες
add_One_or_minusOne(newList)

# Μέθοδος που λαμβάνει την λίστα και τις διαστάσεις m και n των πινάκων
# και επιστρέφει τους πίνακες γεμάτους με τα στοιχεία τους
A, b, c, Eqin = insertIntoTables(newList, m, n)

# Μέθοδος που βρίσκει αν το πρόβλημα είναι min ή max 
# Εφόσον έχει ελεγθεί πιο πριν ότι υπάρχει η λέξη min ή max
MinMax = getMinMax(newList)

# Βαζω τα αποτελέσματα σε πίνακες τύπου array για καλύτερο οπτικό αποτέλεσμα
A_array = [[0 for i in range(n)] for j in range(m)]  
b_array = [[0 for i in range(1)] for j in range(m)] 
c_array = [[0 for i in range(n)] for j in range(1)] 
Eqin_array = [[0 for i in range(1)] for j in range(m)]   

for i in range(m):
    for j in range(n):
        A_array[i][j] = A.iloc[i][j]
        
for i in range(m):
   b_array[i][0] = b.iloc[i][0]
   
for j in range(n):
   c_array[0][j] = c.iloc[0][j]
   
for i in range(m):
   Eqin_array[i][0] = Eqin.iloc[i][0]

# Μετατροπή των πινάκων απο γραμμική μορφή σε δυϊκή

# Βοηθητικός πίνακας temp για την εύκολη εναλλαγή των πινάκων b και c
temp = c_array
c_array = b_array
b_array = temp

# Βοηθητικός πίνακας temp για να αναστρέψουμε τον πίνακα Α
temp = A_array
A_array = [[0 for i in range(m)] for j in range(n)]  

for i in range(m):
    for j in range(n):
        A_array[j][i] = temp[i][j]
        
# Τελικά οι πίνακες A_array, b_array, c_array περιέχουν
# τις ανάλογες παραμέτρους για τον δυϊκό πίνακα

# Καταγράφει τα αποτελέσματα σε μια μεταβλητή τύπου String
# και έπειτα εγγράφονται στο LP-3.txt
text = ''

if MinMax == 1:
    text += 'min z='
else:
    text += 'max z='

# Κρατάει ποιο w ειναι δηλαδη w1 ή w2 ...
count = 1
for i in c_array:
    if i[0] > 0:
        if count != 1:
            text += ' +' + str(i[0]) + 'w' + str(count)
        else:
            text += ' ' + str(i[0]) + 'w' + str(count)
    elif i[0] < 0:
        text += ' ' + str(i[0]) + 'w' + str(count)
    count +=1

text += ('\nst\n')

for i in range(n):
    # Κρατάει ποιο w ειναι δηλαδη w1 ή w2 ...
    count = 1
    for j in range(m):
        if A_array[i][j] > 0:
            if count != 1:
                text += ' +' + str(A_array[i][j]) + 'w' + str(count)
            else:
                text += ' ' + str(A_array[i][j]) + 'w' + str(count)
        elif A_array[i][j] < 0:
            text += ' ' + str(A_array[i][j]) + 'w' + str(count)
        else:
            text += '     '
        count +=1
        
    # Εφόσον γνωρίζουμε οτι οι μεταβλητές είναι ολες >= 0 θα ισχύει:
    if MinMax == -1:
        text += ' <= '
    else:
        text += ' >= '
    
    # Στο τέλος κάθε γραμμής προσθέτουμε τον b όρο
    text += str(b_array[0][i]) + '\n'
        
text += 'end\n\n'

# Προσθέτουμε στο αρχείο τους περιορισμούς των νέων μεταβλητών 
# που προκύπτουν από τις παρακάτω προυποθέσεις
if MinMax == -1:
    # Κρατάει ποιο w ειναι δηλαδη w1 ή w2 ...
    count = 1
    for i in Eqin_array:
        if count == 1:
            text += 'w' + str(count)
        else:
            text += ', w' + str(count)
        
        if(i[0] == -1):
            text += ' >= 0 '
        elif(i[0] == 0):
            text += ' free '
        elif(i[0] == 1):
            text += ' <= 0 '
        
        count += 1
else:
    # Κρατάει ποιο w ειναι δηλαδη w1 ή w2 ...
    count = 1
    for i in Eqin_array:
        if count == 1:
            text += 'w' + str(count)
        else:
            text += ', w' + str(count)
        
        if(i[0] == -1):
            text += ' <= 0 '
        elif(i[0] == 0):
            text += ' free '
        elif(i[0] == 1):
            text += ' >= 0 '
            
        count += 1
    
# Open file to write
file = open('LP-3.txt','w')

# Write into the file
file.write(text) 

# Close the file
file.close()