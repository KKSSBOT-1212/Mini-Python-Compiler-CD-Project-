from sys import stdin
import re

lines=[]

is_int=lambda x: bool(re.match("[0-9]+", x))

is_float=lambda x: bool(re.match("[0-9]+\.[0-9]+", x))

is_variable= lambda x: bool(re.match("[a-zA-Z_][a-zA-Z0-9_]*", x))

is_str= lambda x: bool(re.match("(\".*\")|(\'.*\')", x))

is_bool = lambda x: x=="True" or x=="False"

is_const = lambda x: is_int(x) or is_bool(x) or is_float(x) or is_str(x)

operators={'+','-','*','/','//','%','in','and','or','|','&','**','^','not','>>','<<',"==","!=",">","<",">=","<="}

for line in stdin:
    temp=line.strip().split("\t")
    if temp!=['']:
        lines.append(temp)


def constant_folding():
    changed=0
    for i in range(len(lines)):
        if lines[i][0] in operators:
            if is_const(lines[i][1]) and is_const(lines[i][2]):
                ans=eval(lines[i][1]+lines[i][0]+lines[i][2])
                changed=1
                lines[i][0]="="
                lines[i][1]=str(ans)
                lines[i][2]=" "
    
    return changed




def constant_propagation():
    d={}
    changed=0
    for i in range(len(lines)):
        #if lines[i][0]=='=' and (is_const(lines[i][1]) or is_variable(lines[i][1])) :
        if lines[i][0]=='=' and (is_const(lines[i][1])) :
            d[lines[i][-1]]=lines[i][1]
            continue
        if lines[i][0]=='if' or lines[i][0]=='if False':
            d={}
            continue
        if is_variable(lines[i][1]):
            if lines[i][1] in d:
                changed=1
                #print("line",lines[i],"being set as",d[lines[i][1]]);
                lines[i][1]=d[lines[i][1]]

        if is_variable(lines[i][2]):
            if lines[i][2] in d:
                changed=1
                lines[i][2]=d[lines[i][2]]

        if lines[i][0]=='Label':
            d={}


    return changed
        


def copy_propagation():

    d={}
    changed=0
    for i in range(len(lines)):
        if lines[i][0]=='=' and is_variable(lines[i][1]) and lines[i][2]==' ' :
            d[lines[i][-1]]=lines[i][1]
            continue
        
        if lines[i][0]=='if' or lines[i][0]=='ifFalse':
            d={}
            continue

        if is_variable(lines[i][1]):
            if lines[i][1] in d:
                changed=1
                lines[i][1]=d[lines[i][1]]

        if is_variable(lines[i][2]):
            if lines[i][2] in d:
                changed=1
                lines[i][2]=d[lines[i][2]]

        if lines[i][0]=='Label':
            d={}
    
    return changed
        


def dead_code_elimination():
    flag=None
    #print("DEAD CODE:")
    i=0
    while i<len(lines):
        if lines[i][3] == flag:
            del lines[i]
            print("deleting when none",i)
            flag=None

        if((lines[i][0] == 'if' and lines[i][1]=='False') or (lines[i][0] == 'ifFalse' and lines[i][1]=='True')):
            while lines[i][0] != 'Label':
                del lines[i]
                #print("deleting 1",i)
            del lines[i]
            #print("deleting ",i)

        if((lines[i][0] == 'if' and lines[i][1]=='True') or (lines[i][0] == 'ifFalse' and lines[i][1]=='False')):
            flag=lines[i][3]
            del lines[i]
            #print("deleting 2",i)
            
        i=i+1

    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            if j>=len(lines):
                break
            
            if(lines[j][0] == 'Label' and lines[j][3] == flag):
                flag=None
            if flag!=None:
                continue
            if(lines[j][0] == 'if' or lines[j][0] == 'ifFalse'):
                flag=lines[j][3]
            if(lines[i][3] == lines[j][1]):
                break
            if(lines[i][0]=="=" and lines[j][0]=="=" and lines[i][3] == lines[j][3]):
                #print("deleting redeclared",lines[i][3],"at",i,j);
                del lines[i]
                

    i = len(lines)-1
    while i >= 0:
        flag = 0
        #print(lines)
        skiplist=['param','call','Label','IfFalse','if','goto','Print']
        if lines[i][0] in skiplist:
            i-=1
            #print("continuing",i,lines[i])
            continue

        for j in range(i+1,len(lines)):
            #print(i,j,flag)
            if(lines[i][3] == lines[j][1]):
                flag += 1
            elif lines[j][0] in skiplist and lines[j][3] == lines[i][3]:
                flag += 1
        if flag == 0 :
            #print("deleting line ",i,"-",lines[i])
            #print("for ",lines[j],'\n')	
            del lines[i]
             
        i-=1

    return 1

'''
for l in range(0,len(lines)):
        print(l," ",lines[l]);
    print();
'''
changed=1
while changed:
    c1=constant_folding()
    c2=constant_propagation()
    c3=copy_propagation()
    
    changed=c1 or c2 or c3

dead_code_elimination()

changed=1 
# after dead_code_elimination, we can still do some constant folding, propagation because, some loop blocks like elif 
# and else can sometimes be eliminated. So can evaluate the expressions, propagate contstants,etc

while changed:
    c1=constant_folding()
    c2=constant_propagation()
    c3=copy_propagation()
    
    changed=c1 or c2 or c3


print('\n'.join(list(map(lambda line:'\t'.join(line),lines))))
