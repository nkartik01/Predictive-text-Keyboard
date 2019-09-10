import mysql.connector as sql
def establish():
    cnxn=sql.connect(user='root',password='')
    cursor=cnxn.cursor(buffered=True)
    try:
        cursor.execute('drop database words')
        cursor.execute('create database words')
    except:
        try:
            cursor.execute('create database words')
        except:
            pass
    cursor.execute('use words')
    cursor.execute('create table nodE_table(nodE_id int primary key,node_data char,parent_node int)')
    cursor.execute('create table node_0(node_id int,node_data char,parent_node int)')
    cursor.execute('create table null_table(node_id int,freq int)')
    cursor.execute('insert into node_table values(0,"\0",0)')
    cnxn.commit()
    cnxn.close()
def start():
    global cnxn
    cnxn=sql.connect(user='root',password='',database='words')
    global cursor
    cursor=cnxn.cursor(buffered=True)
def in_list(node_id,word):
    start()
    if(len(word)!=0):
        cursor.execute('select node_id from node_0 where node_data="'+str(word[0])+'"')
        a=cursor.fetchall()
        a=str(a)[2:-3:]
        if(str(a)!=''):
            return(in_list(int(a),word[1::]))
        else:
            return(False)
    else:
        cursor.execute('select node_id from node_'+str(node_id)+' where node_data="\0"')
        a=cursor.fetchall()
        a=str(a)[2:-3:]
        if(str(a)!=''):
            return(True)
        else:
            return(False)
    close()
def insert1(string):
    start()
    cursor.execute("select node_data from node_0")
    insert(0,string)
    close()
def insert(node_id,string):
    if(len(string)!=0):
        cursor.execute('select node_data from node_'+str(node_id))
        child=cursor.fetchall()
        child=str(child)[3:-4:]
        child=child.split("',), ('")
#        #print(child)
        if(string[0] in child):
            cursor.execute("select node_id from node_"+str(node_id)+" where node_data='"+str(string[0])+"'")
            i=cursor.fetchone()
            i=int(str(i)[1:-2:])
            insert(i,string[1::])
            """i=root.dchild.index(string[0])
            insert(root.child[i],string[1::])"""
        else:
            cursor.execute('select count(node_id) from node_table')
            n=cursor.fetchone()
            n=int(str(n)[1:-2:])
            cursor.execute('insert into node_'+str(node_id)+' values('+str(n)+",'"+string[  0]+"',"+str(node_id)+")")
            cursor.execute("insert into node_table values("+str(n)+",'"+string[0]+"',"+str(node_id)+")")
            cursor.execute("create table node_"+str(n)+"(node_id int primary key,node_data char unique,parent_node int)")
            insert(n,string[1::])
            #cursor.execute('')
    else:
        cursor.execute('select node_data from node_'+str(node_id))
        child=cursor.fetchall()
        child=str(child)[3:-4:]
        child=child.split("',), ('")
        #print(child)
        if '\\x00' in child:
            #print("he")
            cursor.execute('select node_id from node_table where node_data="\0" and parent_node='+str(node_id))
            a=cursor.fetchall()
            #print('a is '+str(a))
            a=int(str(a)[2:-3:])
            cursor.execute('update null_table set freq=freq+1 where node_id='+str(a))
        else:
            cursor.execute('select count(node_id) from node_table')
            n=cursor.fetchone()
            n=int(str(n)[1:-2:])
            cursor.execute('insert into node_'+str(node_id)+' values('+str(n)+',"\0",'+str(node_id)+')')
            cursor.execute('insert into node_table values('+str(n)+',"\0",'+str(node_id)+')')
            cursor.execute('insert into null_table values('+str(n)+',0)')
            #print("she")
def close():
    cnxn.commit()
    cnxn.close()
        # def inorder(root):
#     for i in root.child:
#         inorder(chi)
#     if(root.rchild!=None):
#         inorder(root.rchild)
def search(root,string,x,word):
#    #print(root,string,x,word,"1")
    if(len(string)!=0):
        if x==0:
            cursor.execute('select node_id from node_table where node_data="'+string[0]+'"')
        else:
            cursor.execute('select node_id from node_'+str(root)+' where node_data="'+string[0]+'"')
        lis=cursor.fetchall()
#        #print(str(lis),2)
        if str(lis)!='[]':
            lis=str(lis)[2:-3:].split(",), (")
            lis=list(lis)
#            #print(lis,3)
            for i in range (len(lis)):
                lis[i]=int(lis[i])
            for i in lis:
                if x!=0:
                    word.append(string[0])
                    search(i,string[1::],1,word)
                else:
                    word=[string[0]]
                    pnode=0;
                    cursor.execute('select parent_node from node_table where node_id='+str(i))
                    pnode=cursor.fetchone()
                    pnode=int(str(pnode)[1:-2:])
#                    #print(pnode,4)
                    while(pnode!=0):
                        cursor.execute('select node_data from node_table where node_id='+str(pnode))
                        pdata=cursor.fetchone()
#                        #print(pdata,5)
                        pdata=str(pdata)[2:-3:]
#                        #print(pdata,6)
                        if(pdata!='\\x00'):
                            word.append(pdata)
                        cursor.execute('select parent_node from nodE_table where node_id='+str(pnode))
                        pnode=cursor.fetchone()
                        pnode=int(str(pnode)[1:-2])
#                        #print(pnode,7)
                    if(len(word)==0):
                        word.append(string[0])
                    else:
                        word=word[::-1]
                    search(i,string[1::],1,word)
        else:
            pass
    else:
        try:
            cursor.execute('select node_id from node_'+str(root))
            lis=cursor.fetchall()
            lis=(str(lis)[2:-3:]).split(",), (")
            lis=list(lis)
            #print(1)
            try:
                cursor.execute('select node_data from node_'+str(root))
                lis2=cursor.fetchall()
                lis2=str(lis2)[3:-4:].split("',), ('")
                lis2=list(lis2)
                ##print(lis,lis2)
                #print(2)
            except:
                pass
            for i in range (len(lis)):
                temp=word.copy()
                if(lis2[i]!='\\x00'):
                    temp.append(lis2[i])
                    search(lis[i],string,1,temp)
                else:
                    try:
                        cursor.execute('select freq from null_table where node_id='+str(lis[i]))
                        try:
                            a=cursor.fetchall()
                            #print(str(a))
                            a=int(str(a)[2:-3])
                            try:
                                lis3[''.join(word)]=int(a)
                            except:
                                pass#print("hi")
                        except:
                            pass
                            #print("pass")
                            ##print(''.join(word))
                    except:
                        pass
                        #print('nothing found',lis1[i])

        except:
            pass
            #print("hi")
def pressed(node,string):
    pass
def search1(word):
    start()
    cursor.execute("select node_data from node_0")
    global lis3
    lis3={}
    search(0,word,0,0)
    close()
    #print(lis3)
    return(lis3)
def import_dict():
    a=''
    a=input()
    while a!='':
        a=input()
        insert1(a)

try:
    start()
    close()
except:
    establish()
#lis3=[]
#establish()
#insert1(input())
#search1(input())
##print(in_list(0,'king'))
#establish()
#import_dict(2)
