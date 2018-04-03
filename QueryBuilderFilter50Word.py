import re
import MySQLdb
db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='tiana')
cursor = db.cursor()
global CON
"""CON='ALL'
CON='START50WORD'
CON='LAST50WORD'
CON='START50SECOND'
CON='LAST50SECOND'
"""

CON='LAST50WORD'
#expression= "OR(AND('six','four','tracking'),AND('will','spine'))"
#expression="four"
#expression="NOT('six')"
#expression="AND('six','four','tracking')"
#expression="OR('six','four','tracking')"
#expression= "NOT(NOT(OR(AND('six','four'),NOT(OR('six,'four')),'tracking')))"
expression="OR('six','four')"
#expression="tracking"

def reduce(expression):
    print 'reduced called=',expression
    if '(' in expression:
        BoolianOperator = expression.split('(')[0]
        print BoolianOperator
        arg_list=[]
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
            #print arg_index, count
            for i in range(len(expression)):
                if expression[i] == '(':
                    break
            get_arg_from = i + 1
            get_arg_to = len(expression) - 1
            #print get_arg_from,get_arg_to
            arg_index = [x - get_arg_from for x in arg_index]
            #print arg_index
            arg_string = expression[get_arg_from:get_arg_to]
            #print arg_string
            if count != 0:
                arg_index.insert(0, 0)
                indices = arg_index
                #print indices
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
                #print arg_list
            else:
                arg_list.append(arg_string)
                print 'Hello Ashish ',arg_list,len(arg_list)
        else:
            print 'Not Expression Breaking....'
            expression = expression.replace("NOT('", "")
            expression = expression.replace("')", "")
            arg_list.append(expression)
            print 'arg_List=',arg_list
    else:
        #single fetch Operation
        print 'Single Keyword search Operation.'
        search_word = []
        search_word.append(expression)
        Result=OR_Query(search_word)
        return Result

    final_arg_List=[]
    List = []
    ListVisit=0
    for each in arg_list:
        print each
        print List
        if '(' in each:
            if BoolianOperator == 'AND':
                ListVisit=1
                if List:
                    print 'Inside AND,List NonEmpty,call Reduce'
                    temp=reduce(each)
                    List = list(set(List) & set(temp))
                else:
                    print 'Inside AND,List Empty,call Reduce'
                    List = reduce(each)
            elif BoolianOperator == 'OR':
                ListVisit=1
                print 'Inside OR, call Reduce'
                temp=reduce(each)
                List = list(set(List) | set(temp))
            elif BoolianOperator == 'NOT':
                ListVisit=1
                print 'Inside NOT call Reduce.'
                temp = reduce(each)
                NotList = list(set(GetAll_Query()) - set(temp))
                print 'Not Operation Result=',NotList
                if List:
                    List = list(set(List) & set(NotList))
                else:
                    List=NotList
                print 'After NOT Operation: ',List
            else:
                print('Do Nothing Reduce .')
        else:
            final_arg_List.append(each)

    if final_arg_List:
        final_List=[]
        if BoolianOperator == 'AND':
            if List:
                print 'Inside AND,List NonEmpty,call AND Function:'
                temp = AND_Query(final_arg_List)
                final_List = list(set(List) & set(temp))
            elif ListVisit==1:
                final_List=[]
            else:
                final_List= AND_Query(final_arg_List)
            print "AND=", len(final_List), final_List
        elif BoolianOperator == 'OR':
            print 'Inside OR,List NonEmpty,call OR Function:'
            temp = OR_Query(final_arg_List)
            final_List = list(set(List) | set(temp))
            print "OR=", len(final_List), final_List
        elif BoolianOperator == 'NOT':
            temp = OR_Query(final_arg_List)
            NotList = list(set(GetAll_Query()) - set(temp))
            if List:
                print 'Not Operation Result=', NotList
                final_List = list(set(List) & set(NotList))
            else:
                final_List=NotList
            print 'After NOT Operation: ', final_List
        else:
            print('Do Nothing.')
        return final_List
    else:
        return List

def AND_Query(arglist):
    l = "','".join(arglist)
    Data = "('" + l + "')"
    if CON=='ALL':
        Query = "select T.FileName from (select FileName,count(distinct Keyword) from jsoncallworddata where Keyword in " \
                + Data + " group by FileName having count(distinct Keyword)= " + str(len(arglist)) + ") as T"
    elif CON=='START50WORD':
        Query = "select T.FileName from (select FileName,count(distinct Keyword) from jsoncallworddata where wordSeq<=50 and Keyword in " \
                + Data + " group by FileName having count(distinct Keyword)= " + str(len(arglist)) + ") as T"
    elif CON=='LAST50WORD':
        Query = "select T.FileName from (select FileName,count(distinct Keyword) from jsoncallworddata where Keyword in " \
            + Data + " group by FileName having count(distinct Keyword)= " + str(len(arglist)) + ") as T"



    elif CON=='START50SECOND':
        Query = "select T.FileName from (select FileName,count(distinct Keyword) from jsoncallworddata where startTime<=50 and Keyword in " \
                + Data + " group by FileName having count(distinct Keyword)= " + str(len(arglist)) + ") as T"
    elif CON=='LAST50SECOND':
        Query = "aaa"
    else:
        print 'No Operation.'

    datalist=Get_Result(Query)
    return datalist

def OR_Query(arglist):
    l = "','".join(arglist)
    Data = "('" + l + "')"
    if CON=='ALL':
        Query = "select distinct FileName from jsoncallworddata where Keyword in " + Data
    elif CON=='START50WORD':
        Query = "select distinct FileName from jsoncallworddata where wordSeq<=50 and Keyword in " + Data
    elif CON=='LAST50WORD':
        Query = "select distinct T2.FileName from (select FileName,max(wordSeq) m from " \
                "jsoncallworddata group by FileName) T1 inner join (select * from jsoncallworddata) as T2 where " \
                "T1.FileName=T2.FileName and T2.wordSeq>(T1.m-50) and T2.Keyword in " + Data
    elif CON=='START50SECOND':
        Query = "select distinct FileName from jsoncallworddata where startTime<=50 and Keyword in " + Data
    elif CON=='LAST50SECOND':
        Query = "select distinct T2.FileName from " \
                "(select FileName,max(startTime) m from jsoncallworddata group by FileName) T1 inner join " \
                "(select * from jsoncallworddata) as T2 where T1.FileName=T2.FileName and T2.startTime>(T1.m-50);" + Data
    else:
        print 'No Operation.'
    datalist=Get_Result(Query)
    return datalist

def GetAll_Query():
    if CON=='ALL':
        Query = "select distinct FileName from jsoncallworddata"
    elif CON=='START50WORD':
        Query = "select distinct FileName from jsoncallworddata wordSeq<=50"
    elif CON=='LAST50WORD':
        Query = "select distinct T2.FileName from " \
                "(select FileName,max(wordSeq) m from jsoncallworddata group by FileName) T1 inner join " \
                "(select * from jsoncallworddata) as T2 where T1.FileName=T2.FileName and T2.wordSeq>(T1.m-50);"
    elif CON=='START50SECOND':
        Query = "select distinct FileName from jsoncallworddata startTime<=50"
    elif CON=='LAST50SECOND':
        Query = "select distinct T2.FileName from " \
                " (select FileName,max(startTime) m from jsoncallworddata group by FileName) T1 inner join " \
                "(select * from jsoncallworddata) as T2 where T1.FileName=T2.FileName and T2.startTime>(T1.m-50);"
    else:
        print 'No Operation.'

    datalist=Get_Result(Query)
    return datalist

def Get_Result(Query):
    try:
        print Query
        cursor.execute(Query)
        print "Query Run Successfully."
        results = cursor.fetchall()
        datalist = []
        if len(results) > 0:
            for i in results:
                datalist.append(i[0])
            print 'Data send from Query=',Query
        else:
            print "list is empty No data."
        return datalist
    except:
        print "Error: unable to fecth data,  "

data=reduce(expression)
print 'Final Result=',len(data)
print data
db.close()
