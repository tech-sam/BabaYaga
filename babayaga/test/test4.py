from subprocess import PIPE,Popen
import shlex

def dump_schema(host_name,database_name,user_name,database_password,table_name):
    # pg_dump -h 127.0.0.1 -U postgres -p 5433  -d public_sumit -n gt_stellarinnovationspv_stellarinnovations > D:\dev-software\adrem\yoyo.sql

    command = 'pg_dump -h {0} -d {1} -U {2} -p 5432 -n {3} --file yomachha.sql'\
    .format(host_name,database_name,user_name,table_name)

    p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
    print p.stdout
    return p.communicate('{}\n'.format(database_password))

	
	

if __name__ == "__main__":

    print "started----"
        #connection3 = psycopg2.connect("host='localhost' port='5432' dbname='devil_app_dev' user='postgres' password='sa'")

    dump_schema('localhost','devil_app_dev','postgres','sa','public')
