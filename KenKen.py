import functools
from functools import reduce

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


def allDiff( constraints, v ):
	# generate a list of constraints that implement the allDiff constraint for all variable combinations in v
	# constraints is a preconstructed list. v is a list of ConstraintVar instances.
	# call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range(len(v)):
        for j in range(len(v)):
            if ( i != j ) :
                constraints.append(BinaryConstraint( v[i],v[j],fn ))

def setUpKenKen( variables, constraints ):
    # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
    # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object

    # Note that I could accomplish the same by hard coding the variables, for example ...
    # A1 = ConstraintVar( [1,2,3],'A1' )
    # A2 = ConstraintVar( [1,2,3],'A2' ) ...
    # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
    # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
    #   but you can see how tedious this would be.

    rows = ['A','B','C']
    cols = ['1','2','3']
    varNames = [ x+y for x in rows for y in cols ]
    for var in varNames:
        variables[var] = ConstraintVar( [1,2,3],var )

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

def setUpSports( variables, constraints):
    people = ["Alex", "Jessica", "Ryan", "Sophie"]
    sports = ["Baseball", "Tennis", "Basketball", "Soccer"]
    for person in people:
        variables[person] = ConstraintVar([x for x in sports], person)

    for person in people:
        peopleRow = []
        for key in variables.keys():
            peopleRow.append(variables[key])
        allDiff(constraints, peopleRow)

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
                shouldKeep = True
        if (shouldKeep == False):
            bc.var1.domain.remove(x)
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

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')

def trySports():
    variables = dict()
    constraints = []
    setUpSports(variables, constraints)

    print("initial domains\n")
    printDomains(variables)

    print("unary constraint Alex\n")
    nodeConsistent(UnaryConstraint(variables['Alex'], lambda x: x != "Soccer"))
    printDomains(variables)

    print("unary constraint Jessica\n")
    nodeConsistent(UnaryConstraint(variables['Jessica'], lambda x: x != "Soccer" and x != "Basketball"))
    printDomains(variables)

    print("unary constraint Ryan\n")
    nodeConsistent(UnaryConstraint(variables['Ryan'], lambda x: x != "Basketball" and x != "Baseball" and x != "Soccer"))
    printDomains(variables)

    for c in constraints:
        Revise( c , variables)
    print("all constraints pass 1\n")
    printDomains( variables )

    for c in constraints:
        Revise( c, variables )
    print("all constraints pass 2 \n")
    printDomains( variables )

    for c in constraints:
        Revise( c, variables )
    print("all constraints pass 3 \n")
    printDomains( variables )

def tryAC3():
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    variables = dict()
    constraints = []
    setUpKenKen( variables, constraints)

    print("initial domains \n")
    printDomains( variables )

    nodeConsistent( UnaryConstraint( variables['A3'], lambda x: x==2 ) )
    print("unary constraint A3\n")
    printDomains( variables )

    ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    constraints.append( BinaryConstraint( variables['A1'], variables['A2'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['A2'], variables['A1'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: x/y == 2 or y/x == 2) )      # Constraint 2
    constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: x/y == 2 or y/x == 2) )
    constraints.append( BinaryConstraint( variables['B2'], variables['B3'], lambda x,y: x/y == 3 or y/x == 3) )      # Constraint 3
    constraints.append( BinaryConstraint( variables['B3'], variables['B2'], lambda x,y: x/y == 3 or y/x == 3) )
    constraints.append( BinaryConstraint( variables['C2'], variables['C3'], lambda x,y: abs(x-y) == 1 ) ) # Constraint 4
    constraints.append( BinaryConstraint( variables['C3'], variables['C2'], lambda x,y: abs(x-y) == 1 ) )

    for c in constraints:
        Revise( c , variables)
    print("all constraints pass 1\n")
    printDomains( variables )

    for c in constraints:
        Revise( c, variables )
    print("all constraints pass 2\n")
    printDomains( variables )

    for c in constraints:
        Revise( c, variables )
    print("all constraints pass 3\n")
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
tryAC3()
print("DOING SPORTS LOGIC PUZZLE")
trySports()