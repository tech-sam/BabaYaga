import json
from subprocess import PIPE, Popen
import shlex

from django.shortcuts import render
from django.http import HttpResponse

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
        hostName = body['hostName']
        port = body['port']
        dbName = body['databaseName']
        userName = body['userName']
        password = body['password']
        schemaName = body['schemaName']
        pgDump(hostName, port, dbName, userName, password, schemaName)
        return HttpResponse("Latest Data Fetched from Stack Overflow")
    except e as Exception:
        return HttpResponse(f"Failed {e}")


def pgDump(host_name, port, database_name, user_name, database_password, schema_name):
    print("inside pdDump")
    print(host_name+" "+port)
    command = 'pg_dump -h {0} -d {1} -U {2} -p {3} -n {4} --file majani-life.sql'\
        .format(host_name, database_name, user_name, port, schema_name)
    print(command)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate('{}\n'.format(database_password))
