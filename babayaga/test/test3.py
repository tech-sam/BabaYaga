import time
import psycopg2
import os

def main():
    connection3 = psycopg2.connect("host='localhost' port='5432' dbname='devil_app_dev' user='postgres' password='sa'")
    cursor5 = connection3.cursor()
    #os.system('pg_dump -U postgres -t public.user_profile devil_app_dev | psql -U postgres -d test_db')
    # 	subprocess.call("pg_dump -h 127.0.0.1 -U postgres -p 5433  -d public_sumit -n gt_stellarinnovationspv_stellarinnovations > D:\All-workspaces\babayaga\yoyo.sql")
    # pg_dump -h 127.0.0.1 -U postgres -p 5433  -d public_sumit -n gt_stellarinnovationspv_stellarinnovations > D:\dev-software\adrem\yoyo.sql

    os.system("pg_dump --host='localhost' --port='5432' --username=postgres --schema=public --file=yoyo.sql")

    current_time = time.strftime("%c")
    connection3.commit()

    print "finish----"






if __name__ == '__main__':
	main()    