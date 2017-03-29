#from Codify.models import Classification, Products, Companies, Brands
#import csv
##from django.core.serializers.json import Serializer as Builtin_Serializer
#from django.utils.encoding import smart_text
import pyodbc, string, random
from multiprocessing import Process, Queue
import csv
import pprint
from collections import defaultdict


#def purge():
#    Classification.objects.all().delete()

#def grab():
#    with open('C:\\Source Control\\MEC-DataIntegration\\PopRocksPrototype\\PopRocksPrototype\\Codify\\static\\Codify\\testing\\KantarClassification20150420_154258_classified.csv', mode='r') as infile:
#        reader = csv.reader(infile)
#        for row in reader:
#            insert, created = Classification.objects.get_or_create(
#                Kantar_Classification_Key=row[0],
#                Kantar_Parent=row[1],
#                Kantar_Brand=row[2],
#                Kantar_Product=row[3],
#                Kantar_Category=row[4],
#                Kantar_MicroCategory=row[5],
#                Kantar_Creative_Name=row[6],
#                Company=row[7],
#                Brand=row[8],
#                Product=row[9],
#                )
#        return insert

#class Serializer(Builtin_Serializer):
#    def get_dump_object(self, obj):
#        metadata = {
#            "pk": smart_text(obj._get_pk_val(), strings_only=True),
#            "model": smart_text(obj._meta),
#        }
#        return dict(metadata.items() + self._current.items())

#def productgrab():
#    with open('C:\\Source Control\\MEC-DataIntegration\\PopRocksPrototype\\PopRocksPrototype\\Codify\\static\\Codify\\testing\\AmgenProducts.csv', mode='r') as infile:
#        reader = csv.reader(infile)
#        for row in reader:
#            insert, created = Products.objects.get_or_create(
#                Productname=row[0],
#                )
#        return insert

#def brandgrab():
#    with open('C:\\Source Control\\MEC-DataIntegration\\PopRocksPrototype\\PopRocksPrototype\\Codify\\static\\Codify\\testing\\AmgenBrands.csv', mode='r') as infile:
#        reader = csv.reader(infile)
#        for row in reader:
#            insert, created = Brands.objects.get_or_create(
#                Brandname=row[0],
#                )
#        return insert

#def companygrab():
#    with open('C:\\Source Control\\MEC-DataIntegration\\PopRocksPrototype\\PopRocksPrototype\\Codify\\static\\Codify\\testing\\AmgenCompanies.csv', mode='r') as infile:
#        reader = csv.reader(infile)
#        for row in reader:
#            insert, created = Companies.objects.get_or_create(
#                Companyname=row[0],
#                )
#        return insert

def jobcall(environment,batch,client_Name,feed_Name,startDate,endDate,email,dateOption,dateSlicer,mediaYear):
    cnxn = pyodbc.connect('driver={SQL Server Native Client 11.0};server=PSCETLP00103\ETLINS01;database=msdb;uid=MECETLUser;pwd=Mec2&4er;')
    cursor = cnxn.cursor()
    jobname = id_generator()
    sqlQuery = ''
    with open('\\\\PSCETLP00103\MECAnalytics\\Client\\All Feeds - Multi Client\\JobCreateProc.sql', mode='r') as inp:
        for line in inp:
            if line == 'GO\n':
                sqlQuery = sqlQuery.replace("XXXXENV",environment)
                sqlQuery = sqlQuery.replace("XXXXBATCH",batch)
                sqlQuery = sqlQuery.replace("XXXXCLIENT",client_Name)
                sqlQuery = sqlQuery.replace("XXXXFEED",feed_Name)
                sqlQuery = sqlQuery.replace("XXXXSTART",startDate)
                sqlQuery = sqlQuery.replace("XXXXEND",endDate)
                sqlQuery = sqlQuery.replace("XXXXEMAIL",email)
                sqlQuery = sqlQuery.replace("XXXXMYEAR",mediaYear)
                sqlQuery = sqlQuery.replace("XXXXDSLICE",dateSlicer)
                sqlQuery = sqlQuery.replace("XXXXDOPT",dateOption)
                sqlQuery = sqlQuery.replace("REPLACEMEWITHRANDOMSTRING",jobname)
                print sqlQuery
                cursor.execute(sqlQuery)
                cursor.commit()
                sqlQuery = ''
            else:
                sqlQuery = sqlQuery + line
    inp.close()


def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def classAct(streamFile, mapFile):
    print('Writing list to csv...')

    new_col = 'new_column'
    fnd_col = 'PlacementID'
    d2 = getKV(mapFile)

    with open(streamFile, 'rb') as infile, open('c:\\mec_workspace\\codify\\test_classified2.csv', 'wb') as outfile:
        data = csv.DictReader(infile)
        header = data.next()
        header[new_col] = ''
        keys = header.keys()
        

        csv_writer = csv.DictWriter(outfile, sorted(keys)) 
        csv_writer.writeheader()

        for row in data:
            output = codify(row, d2, fnd_col, new_col)
            csv_writer.writerow(output)


def getKV(getKVmapFile):
	kv = []
	with open(getKVmapFile, mode='r') as infile:
		kv = csv.reader(infile)
		dic = {}
		for row in kv:
			dic[row[0]] = row[1]
	return dic


def codify(dict1, dict2, colkey, colnew):
	dict1[colnew] = ''
	for k_d2 in dict2:
		if dict1[colkey]== k_d2:
			dict1[colnew] = dict2[k_d2]
	return dict1


