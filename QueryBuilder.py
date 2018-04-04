#import Python Library.
import re
import MySQLdb

#Open database Connection.
db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='tiana')
cursor = db.cursor()

# Create exxpression..
expression= "NOT(AND(OR('six','four','tracking'),AND('will','spine')))"
#expression="NOT(NOT('six'))"

# Expression Reduce function.
def reduce(expression):
    """
    This is main function which runs recursively,which break the expression
    and stores all arguments in list called arg_list.
    expression: type String:
    return: call_id List of call IDs String:
    """
    print('reduced called:')
    print(expression)
    #Check expression is single keyword fetch or with algebric expression.
    if '(' in expression:
        #Extract Outer Boolean Operator of the expression.
        BooleanOperator = expression.split('(')[0]
        print(BooleanOperator)
        arg_list=[]
        #Check single parameter or not.
        if ',' in expression :
            num_arguments = expression.count(',') + 1
            flag = 0
            count = 0
            arg_index = []
            for i in range(len(expression)):
                if expression[i] == '(':
                    flag += 1
                if expression[i] == ')':
                    flag -= 1
                if flag == 1 and expression[i] == ',':
                    count += 1
                    arg_index.append(i)
            for i in range(len(expression)):
                if expression[i] == '(':
                    break
            get_arg_from = i + 1
            get_arg_to = len(expression) - 1
            arg_index = [x - get_arg_from for x in arg_index]
            arg_string = expression[get_arg_from:get_arg_to]
            if count != 0:
                arg_index.insert(0, 0)
                indices = arg_index
                parts = [arg_string[i:j] for i, j in zip(indices, indices[1:] + [None])]
                removeComma=[]
                for i in parts:
                    if i[0]==',':
                        removeComma.append(i.strip(i[0]))
                    else:
                        removeComma.append(i)
                for i in removeComma:
                    if '(' not in i:
                        arg_list.append(i.strip("'"))
                    else:
                        arg_list.append(i)
            else:
                arg_list.append(arg_string)
        else:
            #if Expression signle parameter then it must be NOT Operation.
            print('Not Expression Breaking....')
            expression = expression.replace("NOT('", "")
            expression = expression.replace("')", "")
            arg_list.append(expression)
            print('arg_List:')
            print(arg_list)
    else:
        #Single Keyword search Operation.
        print('Single Keyword search Operation.')
        search_word = []
        search_word.append(expression)
        Result=OR_Query(search_word)
        return Result

    final_arg_List=[]
    List = []
    ListVisit=0

    for each in arg_list:
        print(each)
        print(List)
        #Check item is expression or not.
        if '(' in each:
            if BooleanOperator == 'AND':
                ListVisit=1
                if List:
                    print('Inside AND,List NonEmpty,call Reduce')
                    temp=reduce(each)
                    List = list(set(List) & set(temp))
                else:
                    print('Inside AND,List Empty,call Reduce')
                    List = reduce(each)
            elif BooleanOperator == 'OR':
                ListVisit=1
                print('Inside OR, call Reduce')
                temp=reduce(each)
                List = list(set(List) | set(temp))
            elif BooleanOperator == 'NOT':
                ListVisit=1
                print('Inside NOT call Reduce.')
                temp = reduce(each)
                NotList = list(set(GetAll_Query()) - set(temp))
                print('Not Operation Result:')
                print(NotList)
                if List:
                    List = list(set(List) & set(NotList))
                else:
                    List=NotList
                print('After NOT Operation:')
                print(List)
            else:
                print('Do Nothing Reduce .')
        else:
            #if item is not expression then stored in Final_arg_List.
            final_arg_List.append(each)

    if final_arg_List:
        final_List=[]
        if BooleanOperator == 'AND':
            if List:
                print('Inside AND,List NonEmpty,call AND Function:')
                temp = AND_Query(final_arg_List)
                final_List = list(set(List) & set(temp))
            elif ListVisit==1:
                final_List=[]
            else:
                final_List= AND_Query(final_arg_List)
        elif BooleanOperator == 'OR':
            print('Inside OR,List NonEmpty,call OR Function:')
            temp = OR_Query(final_arg_List)
            final_List = list(set(List) | set(temp))
        elif BooleanOperator == 'NOT':
            temp = OR_Query(final_arg_List)
            NotList = list(set(GetAll_Query()) - set(temp))
            if List:
                final_List = list(set(List) & set(NotList))
            else:
                final_List=NotList
        else:
            print('Do Nothing.')
        return final_List
    else:
        return List

def AND_Query(arglist):
    """
    This function perform AND Operation.
    arglist : data item in List.
    return : Call_id List.
    """
    line = "','".join(arglist)
    Data = "('" + line + "')"
    Query = "select T.FileName from (select FileName,count(distinct Keyword) from jsoncallworddata where Keyword in "\
            + Data + " group by FileName having count(distinct Keyword)= " + str(len(arglist)) + ") as T"
    datalist=Get_Result(Query)
    return datalist

def OR_Query(arglist):
    """
    This function perform OR Operation.
    arglist : data item in List.
    return : Call_id List .
    """
    line = "','".join(arglist)
    Data = "('" + line + "')"
    Query = "select distinct FileName from jsoncallworddata where Keyword in " + Data
    datalist=Get_Result(Query)
    return datalist

def GetAll_Query():
    """
    This function perform ALL Operation.
    return : ALL Call_id in List.
    """
    Query = "select distinct FileName from jsoncallworddata"
    datalist=Get_Result(Query)
    return datalist

def Get_Result(Query):
    """
    This Function Execute mysql query and return call_id in List.
    Query: 'select * from TableName' type string .
    Return: call_id List as output of Query.
    """
    try:
        cursor.execute(Query)
        print("Query Run Successfully.")
        results = cursor.fetchall()
        datalist = []
        if len(results) > 0:
            for i in results:
                datalist.append(i[0])
            print('Data send from Query:')
            print(Query)
        else:
            print("list is empty No data.")
        return datalist
    except:
        print("Error: unable to fecth data.")

#reduce function calling....
data=reduce(expression)
#Result stored in data variable in List.
print('Final Result:',end=' ')
print(len(data))
print(data)
#Closed Database connection.
db.close()
