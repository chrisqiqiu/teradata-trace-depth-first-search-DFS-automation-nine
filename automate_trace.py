import teradatasql
import pandas as pd
import re

from notification import SlackNotification

from getpass import getpass
import readline
readline.parse_and_bind("control-v: paste")

user = input("Pls enter your Teradata username: ")
TERADATA_PWD = getpass("Pls enter your Teradata password: ")
trace_obj = input("Which table/view you want to trace: ")



host = 'ffxedwprod.ffx.jfh.com.au'
project = "automate trace script"
level=" "*4

slackBot = SlackNotification(__name__)

try:
    connection=teradatasql.connect(host=host, user=user, password=TERADATA_PWD, logmech = 'LDAP')
except Exception as e:
    print("connection fail: " + str(e)) 
    connection.close()
    slackBot.warn("connection fail: " + str(e))
    input('Teradata trace connection step failed. Please screenshot and copy the error message to Chris. Press ENTER to exit')

def main():
    
    no_of_level= 1
    traced=set()

    print("- "+trace_obj)
    with open(f"{trace_obj}.md", 'a', newline="") as f:
                f.write("- "+trace_obj + "\r\n")
    dive(1,traced, trace_obj)
        
def dive(no_of_level,traced, parent_obj ):
    
    child_objs = expand_to_child_tables(parent_obj)
    for obj in child_objs:
        # print(child_objs)
        if obj not in traced  :
            with open(f"{trace_obj}.md", 'a', newline="") as f:
                f.write(level*(no_of_level)+"- "+obj + (" [mds]" if "1011_" in obj else "")  + "\r\n")
            print(level*(no_of_level)+"- "+obj+ (" [mds]" if "1011_" in obj else "") )
            traced.add(obj)
            dive(no_of_level+1, traced, obj)
        else:
            print(level*(no_of_level)+"- "+obj+ (" [mds]" if "1011_" in obj else "") + " **traced above**")
            with open(f"{trace_obj}.md", 'a', newline="") as f:
                f.write(level*(no_of_level)+"- "+obj + (" [mds]" if "1011_" in obj else "")  + " **traced above**\r\n")

def expand_to_child_tables(obj):
    table_name_without_schema = re.search(r".*\.(.*)",obj  ,re.I).group(1)
    df= None
    if re.match(r'^.*_view\..*$', obj ,re.I  ) :
        
        df = pd.read_sql_query(f"""show view {obj}""", connection)
        tx_view=df.iloc[0,0]
        tx_view = re.sub(r"\/\*.*?\*\/", '', tx_view) 
        
        allmatches= re.findall( r'((left|inner|left outer) join|from|join)[ \r\n]+?(prod_[^\s]+?\. *?[^\s]+?)[ \r\n]', tx_view, re.M|re.I)
     
        allmatches= [ i[2].strip().strip(",)(;").replace(" ","") for i in allmatches ]
        
        if len(allmatches)> 0: 
            base_table= allmatches[0]
            final_list= list(set( filter( lambda a : '.' in a and re.match(r'^[\w\.]+$', a ) is not None, allmatches ) ) )   
            final_list.insert(0,  final_list.pop(final_list.index(base_table) )  )
        else :
            final_list=[]
    else:
        df = pd.read_sql_query(f"""
        select  ctl_id, in_db_name, in_object_name, target_tableName
        from prod_gcfr_view.GCFR_Process
        where out_object_name like '%{table_name_without_schema}%'
         and stream_key <> '9999'
         and target_tablename = '{table_name_without_schema}'
         order by ctl_id """, connection)
        final_list=  [a+"."+b for a,b in zip ( df["In_DB_Name"].to_list(), df["In_Object_Name"].to_list() ) ]
    
    return list(filter(lambda x: x!='prod_gcfr_view.GCFR_Stream_Id_Log' 
                       and x!="." 
                       and re.match('^.*(BKEY_|BMAP_).*$', obj ,re.I  ) is None 
                       and x!="prod_prstn_trnsfrm_view.ad_order_header_date_1004"
                                     ,final_list ) )
    

if __name__ == '__main__':
    try:
        main()
        connection.close()
        print(f"\n====================================================\nSuccessfully completed Teradata trace. Please find markdown file named {trace_obj}.md in the same folder as this execution file.")
        input('Press ENTER to exit')
    except Exception as e:
        print("main() fail: " + str(e)) 
        connection.close()
        slackBot.warn("main() fail: " + str(e))
        input('Teradata trace failed. Please screenshot and copy the error message to Chris. Press ENTER to exit')