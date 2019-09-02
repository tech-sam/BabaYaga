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
    # password = params['password']
    schema_name = params['schemaName']
    command = 'pg_dump -h {0} -d {1} -U {2} -p {3} -n {4} -Fc -f {4}.dmp'\
        .format(host_name, database_name, user_name, port, schema_name)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    print(p_status)
    print(output)
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
    file = params['schemaName']
    print("--path for restore file ----")
    cwd = os.getcwd()
    files = os.listdir(cwd)
    print("Files in %r: %s" % (cwd, files))

    command = 'pg_restore -h {0} -d {1} -U {2} {3}.dmp'\
              .format(host_name, database_name, user_name, file)

    command = shlex.split(command)

    # Let the shell out of this (i.e. shell=False)
    p = Popen(command, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    print(p_status)
    print(output)
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
        schema_list = []
        keys = range(total_schemas)
        for i in keys:
            dicts = {}
            dicts['key'] = i
            dicts['schemaName'] = ''.join(
                e for e in schema_records[i] if e.isalnum())
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
