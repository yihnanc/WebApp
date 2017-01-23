from django.shortcuts import render

# Create your views here.

def calculate(request):
    context = {}
#context['show'] is used to record the data which will be shown to the user    
    context['show'] = '0'

# We use size to identify whether this is the first time we linked to calculator or not
# If the size is 0 means, there is no request, and we can judge this is the first time
    size = len(request.POST)

#context['record'] is used to record data which is used to calculate the input    
    context['record'] = ''

#context['minus'] used to store the minus op just for the first time(-1 means postive,1 means negative)
    context['negative'] = '-1'

#This flag is used to identify whether the input is a digit
    flag_num = -1
#This flag is used to identify whether the input is an operator
    flag_syn = -1 

    numbers = ['zero','one', 'two', 'three','four','five','six','seven','eight','nine']
    ops = ['divide','multiply','add','minus','equal']

#record the negative for the first number
    if 'neg' in request.POST:
        context['negative'] = request.POST['neg']

#identify whether the input is an number or not
    if 'rec' in request.POST:
        context['record'] = request.POST['rec']
    for number in numbers:
        if number in request.POST:
            context['record'] = context['record'] + request.POST[number]
            flag_num = 0
            for op in ops:
                if op in context['record']:
                    sep = context['record'].split(op)
                    context['show'] = sep[1]
                    if op == 'equal':
                        context['record'] = context['show']
                    flag_num = 1
                    break
            break

    if flag_num == 0:
            context['show'] = context['record']

#identify whether the input is operator or not  

    if flag_num < 0:
        for op in ops:
            if op in request.POST:
                flag_syn = 0
                for op2 in ops:
                #deal with the case xxx+yyy and xxx+ in context['record']
                    if op2 in context['record']:
                        #deal with the case xxx+, and the current input is also an op, so replace it
                        if context['record'].endswith(op2):
                            context['show'] = context['record'].strip(op2)
                            context['record'] = context['show']+op
                            flag_syn = 1
                            break
                        #deal with the case xxx+yyy    
                        else:
                            sep = context['record'].split(op2)
                            #deal with divde 0
                            if op2 == 'divide' and sep[1] == '0':
                                flag_syn = -1
                                break
                            arg1 = int(sep[0])
                            arg2 = int(sep[1])
                            if context['negative'] == '1':
                                arg1 = -arg1
                                context['negative'] = '-1'
                            res = {
                                'divide' : lambda x,y: x/y,
                                'multiply' : lambda x,y: x*y,
                                'add' : lambda x,y: x+y,
                                'minus' : lambda x,y: x-y
                            }[op2](arg1,arg2)
                            flag_syn = 2
                            print("res is:%d"%res)
                            context['show'] = str(int(res))
                            context['record'] = context['show']+op
                            break
                if flag_syn == 0:
                    # this condition is used to identify whether the current context is -x + or not
                    if context['record'] != '':
                        if context['negative'] == '1':
                            context['show'] = '-'+context['record']
                        else:    
                            context['show'] = context['record']
                        context['record'] = context['record'] + op
                    else:
                        #this condition means the '-' is the first input, which means the user want to input a negative number(if users type in multipe minus,it might be positive)
                        if op == 'minus':
                            context['negative'] = str(-int(context['negative']))
                        #if the user type in an operator which is not minus, context['negative'] must be -1
                        else:
                            context['negative'] = -1                            
                        context['record'] = ''
                break 

    if flag_num < 0 and flag_syn < 0:
        if 'clear' in request.POST:
            context['show'] = '0'
            context['record'] = ''
        else:
            #if size is not zero, and the request also doesn't match for any of our input button, the request must be invalid
            if size != 0:
                context['show'] = 'Error'
                context['record'] = ''
            
    return render(request, 'home.html', context)
