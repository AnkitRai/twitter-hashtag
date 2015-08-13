
# coding: utf-8



from pyproj import Proj, transform # need to import the libaray
import csv

path = '/Users/ankitrai/Downloads/RE__Human_Preference_model-_September_demo/Vectorized_raingarden_final_coordinates.csv'

   




# open the file in read mode:
x = []
y = []
with open(path,'rb') as f:
    next(f)
    readLine = csv.reader(f)
    for row in readLine:
        rows = [row[4],row[5]]
        #print rows
        x.append(rows[0])
        y.append(rows[1])
f.close()        




inProj = Proj(init='epsg:3857')# input projection
outProj = Proj(init='epsg:4326') # output projection




Projected_xy = []

for i in range(len(x)):
    Projected_xy.append(transform(inProj,outProj,x[i],y[i]))  
    




with open('/Users/ankitrai/Downloads/lat_long.csv','wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
                            
    for j in range(len(Projected_xy)):
        #print Projected_xy[j]
        spamwriter.writerow(Projected_xy[j])
csvfile.close()
        











