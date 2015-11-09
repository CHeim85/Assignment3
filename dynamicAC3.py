import functools
from functools import reduce
from testRead import *

# GROUP
# Trey Leuenberger
# Nikita Yurkov
# Colin Heim
# Dillon Littlefield

# This is demonstrating a "class" implementation of AC3. You can accomplish the same with lists. For the project, you can choose either.

# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value

class ConstraintVar:
	# instantiation example: ConstraintVar( [1,2,3],'A1' )
	# MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__(self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.var = v
        self.func = fn

class BinaryConstraint:
	# v1 and v2 should be of class ConstraintVar
	# fn is the lambda expression for the constraint
	# instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

class TernaryConstraint:
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3
        self.func = fn



def allDiff( constraints, v ):
	# generate a list of constraints that implement the allDiff constraint for all variable combinations in v
	# constraints is a preconstructed list. v is a list of ConstraintVar instances.
	# call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range(len(v)):
        for j in range(len(v)):
            if ( i != j ) :
                constraints.append(BinaryConstraint( v[i],v[j],fn ))

def allDiffTC( constraints, v ):
	# generate a list of constraints that implement the allDiff constraint for all variable combinations in v
	# constraints is a preconstructed list. v is a list of ConstraintVar instances.
	# call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y,z: x != y != z
    for i in range(len(v)):
        for j in range(len(v)):
            for k in range(len(v)):
                if ( i != j != k ) :
                    constraints.append(TernaryConstraint( v[i],v[j], v[k], fn ))

# def setUpKenKen( variables, constraints ):
#     # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
#     # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object
#
#     # Note that I could accomplish the same by hard coding the variables, for example ...
#     # A1 = ConstraintVar( [1,2,3],'A1' )
#     # A2 = ConstraintVar( [1,2,3],'A2' ) ...
#     # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
#     # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
#     #   but you can see how tedious this would be.
#
#     rows = ['A','B','C', 'D']
#     cols = ['1','2','3', '4']
#     varNames = [ x+y for x in rows for y in cols ]
#     for var in varNames:
#         variables[var] = ConstraintVar( [1,2,3,4],var )
#
#     # establish the allDiff constraint for each column and each row
#     # for AC3, all constraints would be added to the queue
#
#     # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...
#     for r in rows:
#         aRow = []
#         for k in variables.keys():
#             if ( str(k).startswith(r) ):
# 		#accumulate all ConstraintVars contained in row 'r'
#                 aRow.append( variables[k] )
# 	#add the allDiff constraints among those row elements
#       #  for i in aRow:
#
#         allDiff( constraints, aRow )

def setUpKenKen( variables, constraints, size ):
    # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
    # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object

    # Note that I could accomplish the same by hard coding the variables, for example ...
    # A1 = ConstraintVar( [1,2,3],'A1' )
    # A2 = ConstraintVar( [1,2,3],'A2' ) ...
    # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
    # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
    #   but you can see how tedious this would be.

    rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    cols = ['1','2','3','4','5','6','7','8','9','10','11','12','13',
            '14','15','16','17','18','19','20','21','22','23','24','25','26']

    rows = rows[0:size]
    cols = cols[0:size]

    varNames = [ x+y for x in rows for y in cols ]
    for var in varNames:
        tempNum = ConstraintVar([x for x in range(1, size+1)], var)
        variables[var] = ConstraintVar( [x for x in range(1,size+1)],var )

    # establish the allDiff constraint for each column and each row
    # for AC3, all constraints would be added to the queue

    # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...
    for r in rows:
        aRow = []
        for k in variables.keys():
            if ( str(k).startswith(r) ):
		#accumulate all ConstraintVars contained in row 'r'
                aRow.append( variables[k] )
	#add the allDiff constraints among those row elements
        allDiff( constraints, aRow )

    # for example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
    for c in cols:
        aCol = []
        for k in variables.keys():
            key = str(k)
            # the column is indicated in the 2nd character of the key string
            if ( key[1] == c ):
		# accumulate all ConstraintVars contained in column 'c'
                aCol.append( variables[k] )
        allDiff( constraints, aCol )





    # for example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
    for c in cols:
        aCol = []
        for k in variables.keys():
            key = str(k)
            # the column is indicated in the 2nd character of the key string
            if ( key[1] == c ):
		# accumulate all ConstraintVars contained in column 'c'
                aCol.append( variables[k] )
        allDiff( constraints, aCol )

#--------------------------------------------------------------------------------------------
#########################            COMPLETE REVISE               ##########################

def Revise( bc, variables ):
	# The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
	# A single BinaryConstraint instance is passed in to this function.
	# MISSSING the part about returning sat to determine if constraints need to be added to the queue

    # copy domains for use with iteration (they might change inside the for loops)
    dom1 = list(bc.var1.domain)
    dom2 = list(bc.var2.domain)

    for x in dom1:
        shouldKeep = False
        for y in dom2:
            if(bc.func(x,y) == True):

                print("got here")
                shouldKeep = True
        #print(len(dom2))
        if (shouldKeep == False):
            print('shouldKeep:', shouldKeep)
            print('removing', x)
            bc.var1.domain.remove(x)
        else:
            print("kept", x)
            #print("REMOVING: " + str(x))
            #printDomains(variables)


def ReviseTC( tc, variables ):
	# The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
	# A single BinaryConstraint instance is passed in to this function.
	# MISSSING the part about returning sat to determine if constraints need to be added to the queue

    # copy domains for use with iteration (they might change inside the for loops)
    dom1 = list(tc.var1.domain)
    dom2 = list(tc.var2.domain)
    dom3 = list(tc.var3.domain)

    for x in dom1:
        shouldKeep = False
        for y in dom2:
            for z in dom3:
                if(tc.func(x,y,z) == True):
                    shouldKeep = True
        #print("got here")
        if (shouldKeep == False):
            #print('removing', x)
            tc.var1.domain.remove(x)
            #print("REMOVING: " + str(x))
            #printDomains(variables)




#>>>>>
        # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
#>>>>>

def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

def printDomains( vars, n=4 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')




def AC3(listNumber):

    data = readKenKen(listNumber)
    print(data)


    # create a dictionary of ConstraintVars keyed by names in VarNames.
    variables = dict()
    constraints = []
    constraintsTC = []
    size = int(data[0][0])
    setUpKenKen( variables, constraints, size)

    #print("initial domains \n")
    #printDomains( variables )


    # for i in data[1:]:
    #     if(len(i) == 4):
    #         pr = i[0]
    #         print(pr)
    #         op = i[1]
    #         v1 = i[2]
    #         print(v1)
    #         v2 = i[3]
    #         print(v2)
    #         if op == '+':
    #            print(v1, v2)
    #            print(variables[v1], variables[v2])
    #            constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x+y == int(pr)))
    #            constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x+y == int(pr)))
    #         elif op == '-':
    #             constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: abs(x-y) == int(pr)))
    #             constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: abs(x-y) == int(pr)))
    #         elif op == '/':
    #             constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x/y == int(pr) or y/x == int(pr)))
    #             constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x/y == int(pr) or y/x == int(pr)))
    #         if op == '*':
    #              constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x*y == int(pr)))
    #              #print('pr', int(pr))
    #              constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x*y == int(pr)))

   #  nodeConsistent( UnaryConstraint( variables['B3'], lambda x: x==1 ) )
   #  nodeConsistent( UnaryConstraint( variables['A4'], lambda x: x==2 ) )
   #  #print("unary constraint B3\n")
   #  #printDomains( variables )
   #
   # #[5,+,A3,A4],[2,/,B2,C2],[4,*,B3,C3],[2,-,C1,D1],[1,-,D2,D3]   [8,*,A1,A2,B1] [8,+,B4,C4,D4]
    for i in data[1:]:
        if(len(i) == 4):
            pr = i[0]
            print(pr)
            op = i[1]
            v1 = i[2]
            print(v1)
            v2 = i[3]
            print(v2)
            if op == '+':
               print(v1, v2)
               print(variables[v1], variables[v2])
               print('pr', pr)
               print('intpr', (int(pr) - 5))
               tempPr = int(pr)
               constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x+y == tempPr and x != y))#int(pr)))
               constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x+y == tempPr and x != y))#int(pr)))
               print('nextpr', pr)
            elif op == '-':
                tempPr3 = int(pr)
                constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: abs(x-y) == tempPr3 and x != y))
                constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: abs(x-y) == tempPr3 and x != y))
            elif op == '/':
                tempPr4 = int(pr)
                constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x/y == int(pr) or y/x == tempPr4 and x != y))
                constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x/y == int(pr) or y/x == tempPr4 and x != y))
            elif op == '*':
                tempPr2 = int(pr)
                constraints.append(BinaryConstraint(variables[v1], variables[v2], lambda x,y: x*y == tempPr2 and x != y))
                #print('pr', int(pr))
                constraints.append(BinaryConstraint(variables[v2], variables[v1], lambda x,y: x*y == tempPr2 and x != y))

    #constraints.append( BinaryConstraint( variables['A3'], variables['A4'], lambda x,y: x+y == 5 ) )
    #constraints.append( BinaryConstraint( variables['A4'], variables['A3'], lambda x,y: x+y == 5 ) )
    #constraints.append( BinaryConstraint( variables['B2'], variables['C2'], lambda x,y: x/y == 2 or y/x == 2) )
    #constraints.append( BinaryConstraint( variables['C2'], variables['B2'], lambda x,y: x/y == 2 or y/x == 2) )
    #constraints.append( BinaryConstraint( variables['B3'], variables['C3'], lambda x,y: x*y == 4 and x != y) )
    #constraints.append( BinaryConstraint( variables['C3'], variables['B3'], lambda x,y: x*y == 4 and x != y) )
    #constraints.append( BinaryConstraint( variables['C1'], variables['D1'], lambda x,y: abs(x-y) == 2 ) )
    #constraints.append( BinaryConstraint( variables['D1'], variables['C1'], lambda x,y: abs(x-y) == 2 ) )
    #constraints.append( BinaryConstraint( variables['D2'], variables['D3'], lambda x,y: abs(x-y) == 1 ) )
    #constraints.append( BinaryConstraint( variables['D3'], variables['D2'], lambda x,y: abs(x-y) == 1 ) )
    constraintsTC.append( TernaryConstraint(variables ['A1'], variables['A2'], variables['B1'], lambda x,y,z: x*y*z == 8 and x != y != z ))
    constraintsTC.append( TernaryConstraint(variables ['A1'], variables['B1'], variables['A2'], lambda x,y,z: x*y*z == 8 and x != y != z))
    constraintsTC.append( TernaryConstraint(variables ['A2'], variables['A1'], variables['B1'], lambda x,y,z: x*y*z == 8 and x != y != z))
    constraintsTC.append( TernaryConstraint(variables ['A2'], variables['B1'], variables['A1'], lambda x,y,z: x*y*z == 8 and x != y != z))
    constraintsTC.append( TernaryConstraint(variables ['B1'], variables['A1'], variables['A2'], lambda x,y,z: x*y*z == 8 and x != y != z))
    constraintsTC.append( TernaryConstraint(variables ['B1'], variables['A2'], variables['A1'], lambda x,y,z: x*y*z == 8 and x != y != z))


    # #[8,+,B4,C4,D4]
    # constraintsTC.append( TernaryConstraint(variables ['B4'], variables['C4'], variables['D4'], lambda x,y,z: x+y+z == 8))
    # constraintsTC.append( TernaryConstraint(variables ['B4'], variables['D4'], variables['C4'], lambda x,y,z: x+y+z == 8))
    # constraintsTC.append( TernaryConstraint(variables ['C4'], variables['B4'], variables['D4'], lambda x,y,z: x+y+z == 8))
    # constraintsTC.append( TernaryConstraint(variables ['C4'], variables['D4'], variables['B4'], lambda x,y,z: x+y+z == 8))
    # constraintsTC.append( TernaryConstraint(variables ['D4'], variables['B4'], variables['C4'], lambda x,y,z: x+y+z == 8))
    # constraintsTC.append( TernaryConstraint(variables ['D4'], variables['C4'], variables['B4'], lambda x,y,z: x+y+z == 8))

    #
    # # nodeConsistent( UnaryConstraint( variables['A3'], lambda x: x==2 ) )
    # # print("unary constraint A3\n")
    # # printDomains( variables )
    # #
    # # ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    # # constraints.append( BinaryConstraint( variables['A1'], variables['A2'], lambda x,y: abs(x-y) == 2 ) )
    # # constraints.append( BinaryConstraint( variables['A2'], variables['A1'], lambda x,y: abs(x-y) == 2 ) )
    # # constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: x/y == 2 or y/x == 2) )      # Constraint 2
    # # constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: x/y == 2 or y/x == 2) )
    # # constraints.append( BinaryConstraint( variables['B2'], variables['B3'], lambda x,y: x/y == 3 or y/x == 3) )      # Constraint 3
    # # constraints.append( BinaryConstraint( variables['B3'], variables['B2'], lambda x,y: x/y == 3 or y/x == 3) )
    # # constraints.append( BinaryConstraint( variables['C2'], variables['C3'], lambda x,y: abs(x-y) == 1 ) ) # Constraint 4
    # # constraints.append( BinaryConstraint( variables['C3'], variables['C2'], lambda x,y: abs(x-y) == 1 ) )
    #
    # nodeConsistent( UnaryConstraint( variables['A1'], lambda x: x==2 ) )
    # nodeConsistent( UnaryConstraint( variables['B3'], lambda x: x==1 ) )
    # nodeConsistent( UnaryConstraint( variables['C3'], lambda x: x==2 ) )
    # print("unary constraint A3\n")
    # printDomains( variables )
    #
    # ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    # constraints.append( BinaryConstraint( variables['A2'], variables['A3'], lambda x,y: x+y == 4 ) )
    # constraints.append( BinaryConstraint( variables['A3'], variables['A2'], lambda x,y: x+y == 4 ) )
    # constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: x+y == 4 ) )      # Constraint 2
    # constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: x+y == 4 ) )
    # constraints.append( BinaryConstraint( variables['B2'], variables['C2'], lambda x,y: abs(x-y) == 1) )      # Constraint 3
    # constraints.append( BinaryConstraint( variables['C2'], variables['B2'], lambda x,y: abs(x-y) == 1) )
    # #constraints.append( BinaryConstraint( variables['B3'], variables['C3'], lambda x,y: x+y == 3 ) ) # Constraint 4
    # #constraints.append( BinaryConstraint( variables['C3'], variables['B3'], lambda x,y: x+y == 3 ) )
    #
    #
    #
    '''
    for c in constraints:
        Revise( c , variables)
    print("all constraints pass 1\n")
    printDomains( variables )

    for tc in constraintsTC:
        ReviseTC( tc, variables )
    print("all constraints pass 2\n")
    printDomains( variables )


    for c in constraints:
        Revise( c , variables)
    print("all constraints pass 1\n")
    printDomains( variables )

    for tc in constraintsTC:
        ReviseTC( tc, variables )
    print("all constraints pass 2\n")
    printDomains( variables )


    for c in constraints:
        Revise( c , variables)
    print("all constraints pass 1\n")
    printDomains( variables )

    for tc in constraintsTC:
        ReviseTC( tc, variables )
    print("all constraints pass 2\n")
    printDomains( variables )
    '''
    #for i in range(0,1):
    for c in constraints:
        Revise( c , variables)
        for tc in constraintsTC:
            ReviseTC( tc, variables )
    printDomains( variables )




    '''
    print('----------------------------------------------------------')
    print('TO DO:')
    print('1) Write the function revise().')
    print('2) Complete the binary constraints for KenKen puzzle.')
    print('3) Run code and confirm that all domains are reduced to single value.')
    print('')
    print('4) Create the variables and constraints for the sport logic puzzle.')
    print('-- Do not hand edit the domains based on Unary constraints. Define those as part of the puzzle.')
    print('5) Solve the puzzle using nodeConsistent() and revise().')

    print(' IF you finish all of that, see if you can frame the person-animal-color puzzle for AC3')

    print('NOTE, the implementation of AC3 requires a queue on which you pop a constraint, then push neighbors if necessary')
    print('   Since this is not implemented here, you can create a "hack" by repeatedly calling Revise.')
    print('----------------------------------------------------------')
    print(' SUBMIT your code via TurnItIn (whatever state it is in when class is over is fine.')
    '''

print("DOING KENKEN")
AC3(0)
