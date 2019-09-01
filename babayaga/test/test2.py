import os
import sys
import subprocess
import tempfile
from datetime import datetime

def main():
	now = datetime.now()
	print now
	dbenv = {"PATH": os.environ["PATH"]}
	print dbenv
	dbenv["PGHOST"] = "localhost"
	dbenv["PGPORT"] = "5433"
	dbenv["PGUSER"] = "postgres"
	logfile = tempfile.TemporaryFile()
	print "-------"
	print logfile
	databases = subprocess.check_output(["psql", "--no-align", "--tuples-only",
        "--command",
        "SELECT datname FROM pg_database WHERE datname NOT IN ('postgres', "
        "'template0','template1')", "postgres"], stderr=subprocess.STDOUT, env=dbenv)

        for db in databases.split():
            print "DB: " + db
        
	
if __name__ == '__main__':
	main()