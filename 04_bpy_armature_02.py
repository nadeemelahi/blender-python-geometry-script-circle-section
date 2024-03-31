
#
# author: Nadeem Elahi
# nadeem.elahi@gmail.com
# nad@3deem.com
# license: gpl v3
# 

import bpy
from math import sin
from math import cos
from math import radians
# from math import sqrt

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj)

# Settings 
name = 'Armature' 
coilCnt = 3
inner = 15  # radius inner
outer = 20 # radius outer

step = 5 
divisions = 3 # 3 going positive, 3 going negative


#   0  1 2 3 4 5  6
# -15 10 5 0 5 10 15 = 3 + 1 + 3
vertsCnt = divisions + 1 + divisions  





# angles

positiveAngles = []
negativeAngles = []
angles = []


for idx in range ( divisions + 1 ):
	positiveAngles.append ( step * idx )
#print ( positiveAngles )

# 5*(3-0) , 5*(3-1) , 5*(3-2) = [ 15 , 10 , 5 ] 
for idx in range ( divisions ):
	negativeAngles.append ( -1 * step * ( divisions - idx ) )
#print ( negativeAngles )

angles = negativeAngles + positiveAngles
# [ -15 , -10 , -5 , 0 , 5 , 10 , 15 ]
#print ( angles )

# convert to radians
for idx in range ( vertsCnt ) :
	angles [ idx ] = radians ( angles [ idx ] )




# verts

verts = []


def vertsByAngleAndRadius ( rad , ang , rot ):
	xloc = rad * cos ( ang + rot ) 
	yloc = rad * sin ( ang + rot )  
	verts.append( [ xloc , yloc , 0 ] )



def armAtRotation ( rot ) :
	for idx in range( vertsCnt ):
		print ( idx )
		vertsByAngleAndRadius ( inner , angles [ idx ] , rot )
		vertsByAngleAndRadius ( outer , angles [ idx ] , rot )







# face 4 verts each 
# [ 0 , 1 , 3 , 2 ]
# [ 2 , 3 , 5 , 4 ]
# ...
# [ 10, 11, 13, 12 ]

faces = []
last = ( vertsCnt * 2 ) - 2

def appendFaces ( offset ) :
	idx = 0
	while ( idx < last ) :
		index = idx + offset * vertsCnt * 2
		faces.append ( [ index , index + 1 , index + 3 , index + 2 ] )
		idx += 2

for idx in range ( coilCnt ) :

	rot = radians ( idx * 360 / coilCnt ) # rotation angle
	armAtRotation ( rot )
	appendFaces ( idx ) 








# FINALLY

# Create Mesh Datablock 
mesh = bpy.data.meshes.new ( name ) 
mesh.from_pydata ( verts, [], faces ) 
# mesh from vertices, edges and faces. 
# if you pass a faces list you can skip edges


# Create Object and link to scene 
obj = bpy.data.objects.new(name, mesh) 
bpy.context.scene.collection.objects.link ( obj ) 


# Select the object 
bpy.context.view_layer.objects.active = obj 
obj.select_set ( True )
bpy.ops.object.mode_set(mode='EDIT')



