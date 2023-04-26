import random

#Global variables
MAX_LINES=3
MAX_BET=1000
MIN_BET=10

ROWS=3
COLS=3

##Probability of every character appearing in a single run of slot machine
symbol_count={'A':2,'B':4,'C':6,'D':8} 

symbol_value={'A':5,'B':4,'C':3,'D':2}


def get_slot_machine_spin(rows,cols,symbols):
    
#storing all the character inside a list so that we can choose randomly
#from them during the run of slot machine
    
    all_symbols=[] #This stores all the character in slot machine run
    for symbol,symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns=[] #stores all the character produced in iteration
    for _ in range(cols):
#column list stores individual row for every iteration which is then appends to columns list
#so columns[] stores all the all rows characters which are randomly picked
        column=[]
#making a copy of all_symbols list so that we can remove the character which have already appeared
#without cauing changes in original list.
        current_symbols=all_symbols[:]
        for _ in range(rows):
            value=random.choice(current_symbols)
#removing the character which have already appreaded(as per thier chances) so they dont
#appear more no. of times then thier original chances(like A should not appear more then 2 times)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

#as we want to print the character Vertically and columns stores values in rows format
#we have to perform transpose of a matrix to print it vertically
def print_slot_machine(columns):#Tranposing 
#suppose columns is like this [['D', 'B', 'D'], ['D', 'C', 'D'], ['C', 'B', 'B']]

    for row in range(len(columns[0])): #from above it will run for 3 iteration
        for i,column in enumerate(columns): #column will point at the ith index of columns
            if i !=len(columns)-1:
                print(column[row],end=' | ') #as column points at 0th index it has ['D', 'B', 'D']
            else:                            #column[0] will print D as so on
                print(column[row],end='') #as we dont want '|' when printing the last column
        print()

#as we are comparing the characters before transposing we have to compare
#1st index from every row to check if a line in slot machine has all 3 characters
#same rather then comparing if all rows have similar values.
#for e.g. we have to if columns[0][0]==columns[1][0]==columns[2][0] (D,D,A)
#columns[0][1]==columns[1][1]==columns[2][1] (B,B,C)
#columns[0][2]==columns[1][2]==columns[2][2] (C,B,D)
        
def check_winnings(columns,lines,bet,values):
#suppose columns is [['D', 'B', 'C'], ['D', 'B', 'B'], ['A', 'C', 'D']],lines=3
    winnings=0
    winning_lines=[]
    for line in range(lines): #range(3)
        symbol=columns[0][line] #from given e.g. this is D
        for column in columns: #column 1st will have ['D', 'B', 'C'] then ['A', 'B', 'B'] &['A', 'C', 'D']
            symbol_to_check=column[line] #for 1st iteration it is D
            if symbol!=symbol_to_check: #for 1st iteration it is D&D,D&A then breaks cuz D!=A
                break
        else:
            winnings+=values[symbol]*bet #winnings will be * by symbol value(e.g. for D * by 2)
            winning_lines.append(line+1)
            
    return winnings,winning_lines

#Function for taking deposit money
def deposit():
    while True:
        amount=input("What would you like to deposit:₹ ")
        if amount.isdigit():
            amount=int(amount)
            if amount>0:
                break
            else:
                print("Amount should be greater then 0.")
        else:
            print("Please enter a number.")
    return amount

#Function for taking the bet amount on each lines
def get_num_of_lines():
    while True:
        lines=input("Enter the number of lines to bet on(1-"+str(MAX_LINES)+")?")
        if lines.isdigit():
            lines=int(lines)
            if 1<=lines<=MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

#Function for Calculating the total bet amount
def get_bet():
    while True: #Making sure total bet amount is not > deposit amount
        amount=input("What would you like to bet on each line:₹ ")
        if amount.isdigit():
            amount=int(amount)
            if MIN_BET<=amount<=MAX_BET:
                break
            else:
                print(f"Amount should be between ₹{MIN_BET}-₹{MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount   

#this function help in running automatically until all deposit money is lost    
def spin(balance):
    lines=get_num_of_lines()
    while True:
        bet=get_bet()
        total_bet=bet*lines
        if total_bet>balance:
            print(f'You dont have enough to bet that amount,your current balance is:₹{balance} ')
        else:
            break
        
    print(f'You are bettting ₹{bet} on {lines} lines.')
    print(f'Your Total bet is equal to:₹{total_bet}')
#calling the get_slot_machine_spin and passing global values 
    slots=get_slot_machine_spin(ROWS,COLS,symbol_count)
####    print(slots) #this is the matrix we performed transpose on
#get_slot_machine_spin returns the columns which is stored in slots in row format
#we passes that in print_slot_machine we performs transpose and prints them in column format
    print_slot_machine(slots)
    winnings,winning_lines=check_winnings(slots,lines,bet,symbol_value)
    print(f'You won ₹{winnings}.')
    print(f'You won on lines:',*winning_lines)
    return winnings - total_bet
    

def main():
    balance=deposit()
    while True:
        print(f'Current balance is ₹{balance}')
        answer=input('Press enter to play(q to quit).')
        if answer=='q':
            break
        if balance==0: #my condition not given in video
            print('You dont have any balance left')
            break
        balance+=spin(balance)
    print(f'You left with ₹{balance}')
main()
