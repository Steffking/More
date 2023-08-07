import re
def checkword(word):
    statements = ['is','and','or','null','trunc', 'where', 'not', 'in', '(']
    for sword in statements:
        if sword in word:
            return True
    return False
def convertExists(query):
    alias = query.split(' ')[(query.split(' ').index('from')+2)]
    query = query[query.find('where')+6:]
    query.replace(alias+".", "%A.")
    return query
#print(convertExists("from blah v where du hu"))
def convert_sql_query(query):
    if ("exists" in query):
        return convertExists(query)    
    newQuery = ""
    query.replace('nvl(:PERSONALUD,berfunc.USER_2_PERSONALID())', 'v_personalid')
    wordarray = query.split(' ')
    for i in range(wordarray.index('where')+1,len(wordarray)):
        if checkword(wordarray[i]):
            newQuery+=" "+wordarray[i]
        else:
            newQuery+=" %A."+wordarray[i]
    #query = query[:query.find('where')]+" "+newQuery
    query = newQuery
    def commas(match):
        char = match.group(1)
        return f"'||chr(39)||'{char}'||chr(39)||'"
    pattern = r"'([A-Za-z])'"
    query = converted_query = re.sub(pattern, commas, query)
    return converted_query

print(convert_sql_query("select count(*) into v_anz from RKABER where RKAABSID is null and Status not in ('S','G') and personalid=v_personalid"))
"""
select count(*) into v_anz from RKABER where RKAABSID is null and Status not in ('S', 'G') and personalid=v_personalid

select count(*) into v_anz from RKABER where RKAABSID is null and Status not in ('||chr(39)||'S'chr(39)||', '||chr(39)||'G'||chr(39)||') and personalid=v_personalid
"""