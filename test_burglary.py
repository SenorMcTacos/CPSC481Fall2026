from probability import *
import sys

sys.path.append("/home/senortaco/Things/School/CPSC491-AI/aima-python/aima/")


T, F = True, False

burglary = BayesNet([
    ('Burglary', '', 0.001),
    ('Earthquake', '', 0.002),
    ('Alarm', 'Burglary Earthquake',
     {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
    ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
    ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
])

#if __name__ == '__main__':

print(enumeration_ask('Burglary', dict(), burglary).show_approx())
print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary))
print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary)[T])

print(burglary.variable_node('Burglary').p(T, {}))
print(burglary.variable_node('Alarm').p(T, {'Burglary': T, 'Earthquake': F}))

