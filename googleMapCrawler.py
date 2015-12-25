import urllib
import PIL
import csv
import re
#base url




def GetStaticMap(filename,gps,zoomin,res_size,imgformat,api_key):
	request = "https://maps.googleapis.com/maps/api/staticmap?maptype=satellite"
	request += "&center= %s" % gps;
	request+="&zoom= %i" %zoomin;
	request+="&size=%ix%i" %(res_size);
	request+="&key= %s" %api_key;

	urllib.urlretrieve(request,filename+"."+imgformat)
	print request;

def read_gps(file_object,loc=[]):
	read_file = csv.reader(file_object)
	for row in read_file:
		pattern = re.search(r"\[(.*?)\]",row)
		loc.append(pattern)
	return loc;
	



if __name__=="__main__":
	path_to_file = "/Users/ankitrai/Desktop/gps_coordinates.csv"
	with open(path_to_file,"rU") as csv_file:
		print csv_file.name
		loc = read_gps(csv_file,loc=[])
	api_key = "AIzaSyDOFEx_RX1k9Dt1Fu82GT9QZQ6bDAv1qX0";
	for item in loc:
		GetStaticMap(str(item),"loc[item]",12,(500,500),"png",api_key)
	