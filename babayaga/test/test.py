from subprocess import PIPE,Popen
import shlex

def dump_table(host_name,database_name,user_name,database_password,table_name):

    command = 'pg_dump -h {0} -d {1} -U {2} -p 5432 -t public.{3} -Fc -f /Users/sumitsharma/Documents/workspace/table.dmp'\
    .format(host_name,database_name,user_name,table_name)

    p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)

    return p.communicate('{}\n'.format(database_password))

def main():
    print ("babayaga main yo")
    dump_table('localhost','public_sumit','postgres','sa','user_profile')
 

if __name__ == "__main__":
    main()
