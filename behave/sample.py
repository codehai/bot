from behave import condition, action, FAILURE
from behave import repeat, forever, succeeder, failer
from behave.core import SUCCESS, FAILURE, RUNNING


@condition
def is_greater_than_10(x):
    return x > 10

@condition
def is_greater_than_20(x):
    return x > 20

@condition
def is_between_0_and_10(x):
    return 0 < x < 10

@action
def wow_greater_than_20(x):
    print("WOW, %d is a large number!" % x)

@action
def wow_large_number(x):
    print("WOW, %d is a large than 20!" % x)


@action
def wow_litter_number(x):
    print("WOW, %d is a litter than 20!" % x)

@action
def doomed(x):
    print ("%d is doomed" % x)
    return FAILURE


@action
def count_from_1(x):
    for i in range(1, x):
        print ("count", i)
        yield
    print ("count", x)



tree = (
    is_greater_than_10 >>  is_greater_than_20 >> wow_greater_than_20 | wow_litter_number
    
    | is_between_0_and_10 >> count_from_1 
    
    | failer * repeat(3) * doomed
)

print (tree)

def my_debugger(node, state):
    print ("[%s] -> %s" % (node.name, state))

bb = tree.debug(my_debugger, 22) # Creates an run instance

# Now let the tree do its job, till job is done
state = bb.tick()
print ("state = %s\n" % state)
while state == RUNNING:
    state = bb.tick()
    print("state = %s\n" % state)
assert state == SUCCESS or state == FAILURE
