import json
from subprocess import PIPE, Popen
import shlex
import psycopg2
from datetime import datetime
from pathlib import Path
import os
import boto3

from botocore.exceptions import NoCredentialsError


from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


from babayaga_app.models import DatabseServerProps
from rest_framework import viewsets, permissions
from .serializers import DbPropsSerialzer


# Create your views here.


def index(request):
    return HttpResponse("Success")


class DbPropsAPI(viewsets.ModelViewSet):
    queryset = DatabseServerProps.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DbPropsSerialzer


def dumpSchema(request):
    try:

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(datetime.now(tz=None))
        data = body['data']
        pgDumpParams = {}
        pgRestoreParams = {}
        for dbProps in data:
            if bool(dbProps.get("sourceDb")):
                sourceDbParams = dbProps.get("sourceDb")
                pgDumpParams['hostName'] = sourceDbParams['hostName']
                pgDumpParams['port'] = sourceDbParams['port']
                pgDumpParams['databaseName'] = sourceDbParams['databaseName']
                pgDumpParams['userName'] = sourceDbParams['userName']
                pgDumpParams['password'] = sourceDbParams['password']
                pgDumpParams['schemaName'] = sourceDbParams['schemaName']
                pgDumpParams['restoreSchema'] = sourceDbParams['restoreSchema']
                pgDumpParams['s3Upload'] = sourceDbParams['s3Upload']

            if bool(dbProps.get("destinationDb")):
                destinationDbparams = dbProps.get("destinationDb")
                pgRestoreParams['hostName'] = destinationDbparams['hostName']
                pgRestoreParams['port'] = destinationDbparams['port']
                pgRestoreParams['databaseName'] = destinationDbparams['databaseName']
                pgRestoreParams['userName'] = destinationDbparams['userName']
                pgRestoreParams['password'] = destinationDbparams['password']
                pgRestoreParams['schemaName'] = destinationDbparams['schemaName']
                pgRestoreParams['updatedSchemaName'] = destinationDbparams['updatedSchemaName']

        print("----pgRestoreParams-----")
        print(pgRestoreParams)
        print("----pgDumpParams-----")
        print(pgDumpParams)
        # return JsonResponse({'completed': 'true'})
        return pgDump(pgDumpParams, pgRestoreParams)

    except e as Exception:
        return HttpResponse(f"Failed {e}")


def pgDump(params, pgRestoreParams):

    host_name = params['hostName']
    port = params['port']
    database_name = params['databaseName']
    user_name = params['userName']
    password = params['password']
    schema_name = params['schemaName']
    env_path = os.environ.get('DUMP_PATH')
    pgRestoreParams['main_schema'] = schema_name
    print("env path "+env_path)
    path_to_file = ""
    if not env_path:
        print("coming to if")
        path_to_file = "/opt/schema-dest/"+schema_name+".dmp"
    else:
       print("coming to else")
       path_to_file = env_path+"/"+schema_name+".dmp" 
    print("path to file "+path_to_file)
    pgRestoreParams.update(schemaName=path_to_file)
    # command = 'pg_dump -h {0} -d {1} -U {2} -p {3} -n {4} -Fc -f {4}.dmp'\
    #     .format(host_name, database_name, user_name, port, schema_name)
    command = 'pg_dump  --dbname=postgresql://{2}:{5}@{0}:{3}/{1}  -n {4} -Fc -f {6}'\
        .format(host_name, database_name, user_name, port, schema_name, password,path_to_file)

    p = Popen(command, shell=True, stdin=PIPE,
              stdout=PIPE, stderr=PIPE, encoding='utf8')
    (outs, errs) = p.communicate('{}\n'.format(password))

    p_status = p.wait()
    print(p_status)
    print(outs)
    changedFileName = pgRestoreParams['updatedSchemaName']
   
    print("--path for actual file ----"+schema_name+".dmp")
    print("--path for changed file ----"+changedFileName+".dmp")
   
    if(True == params['restoreSchema']):
        restore_table(pgRestoreParams)
    if(True == params['s3Upload']):
        uploadToS3(schema_name+".dmp")

    return JsonResponse({'completed': 'true'})


def restore_table(params):
    print("----restore schema called----")
    host_name = params['hostName']
    port = params['port']
    database_name = params['databaseName']
    user_name = params['userName']
    database_password = params['password']
    main_schema = params['main_schema']
    file = params['schemaName']
    changedSchemaName = params['updatedSchemaName']
    print("file to be restore pg_restore "+file)
	
    
    cwd = os.getcwd()
    files = os.listdir(cwd)
    print("Files in %r: %s" % (cwd, files))

    # command = 'pg_restore -h {0} -d {1} -U {2} -p {3} {4}.dmp'\
    #           .format(host_name, database_name, user_name, port, file)

    command = 'pg_restore -j 8 --dbname=postgresql://{2}:{5}@{0}:{3}/{1} {4}'\
              .format(host_name, database_name, user_name, port, file, database_password)

    command = shlex.split(command)

    # Let the shell out of this (i.e. shell=False)
    p = Popen(command, shell=False, stdin=PIPE,
              stdout=PIPE, stderr=PIPE, encoding='utf8')
    (outs, errs) = p.communicate('{}\n'.format(database_password))
    try:
        connection = psycopg2.connect(user=user_name,
                                      password=database_password,
                                      host=host_name,
                                      port=port,
                                      database=database_name)
        update_schema_name = "ALTER SCHEMA "+ main_schema +" RENAME TO "+changedSchemaName
        cursor = connection.cursor()
        cursor.execute(update_schema_name)
        connection.commit()
        count = cursor.rowcount
        print(schema, "Record Updated successfully ")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            

    p_status = p.wait()
    print(p_status)
    print(outs)
    # p.communicate('{}\n'.format(database_password))


def uploadToS3(file):
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    bucket = os.environ.get('AWS_S3_BUCKET')
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    print("-----coming to s3-----")
    print(os.environ)
    print('---ACCESS_KEY---')
    print(os.environ.get('AWS_ACCESS_KEY'))

    print('---SECRET_KEY---')
    print(os.environ.get('AWS_SECRET_KEY'))

    print('---AWS_S3_BUCKET---')
    print(os.environ.get('AWS_S3_BUCKET'))

    try:
        s3.upload_file(file, bucket, file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def getSchemas(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        hostName = body['hostName']
        port = body['port']
        dbName = body['databaseName']
        userName = body['userName']
        password = body['password']
        connection = psycopg2.connect(user=userName,
                                      password=password,
                                      host=hostName,
                                      port=port,
                                      database=dbName)
        cursor = connection.cursor()
        postgreSQL_select_Query = "select schema_name from information_schema.schemata WHERE schema_name !~* 'pg_.*|.*information_schema.*'"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from information_schema using cursor.fetchall")
        schema_records = cursor.fetchall()
        total_schemas = len(schema_records)
        print("ccccccccccc")
        print(total_schemas)
        schema_list = []
        keys = range(total_schemas)
        for i in keys:
            dicts = {}
            dicts['key'] = i
            #print(schema_records[i])
            dicts['schemaName'] = ' '.join(schema_records[i])
            print(' '.join(schema_records[i]))
            dicts['hostName'] = hostName
            dicts['port'] = port
            dicts['databaseName'] = dbName
            dicts['userName'] = userName
            dicts['password'] = password
            schema_list.append(dicts)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return JsonResponse(schema_list, safe=False)


