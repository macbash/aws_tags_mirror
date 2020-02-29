import boto3
import sys, getopt
global ec2
ec2 = boto3.client("ec2")
def getres(sourceInstance):
	reservations =   ec2.describe_instances(Filters=[{'Name': 'instance-id','Values': [sourceInstance]}])["Reservations"]
	return reservations

tag = []

try:
   opts, args = getopt.getopt(sys.argv[1:],"hs:d:",["source=","destination="])
except getopt.GetoptError:
   print 'tags.py -i <source> -d <destination>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'tags.py -i <source> -d <destination>'
      sys.exit()
   elif opt in ("-s", "--source"):
      sourceInstance = arg
   elif opt in ("-d", "--destiantion"):
      destinationInstance = arg
print 'Source Resource =', sourceInstance
print 'Destination Resource =', destinationInstance 

#sourceInstance = sys.argv[1]
#destinationInstance = sys.argv[2]

for reservation in getres(sourceInstance):
    for each_instance in reservation["Instances"]:
	for tags in each_instance["Tags"]:
		if tags["Key"] != "Name":
			tag.append({'Key': tags["Key"], 'Value': tags["Value"]})

for reservation in getres(destinationInstance):
    for each_instance in reservation["Instances"]:
	ec2.create_tags( Resources = [each_instance["InstanceId"] ], Tags = tag )

