#coding=utf-8
import sys
import bpy
import math
import random
import colorsys
import os
import mathutils
import numpy as np
from random import randint

sys.path.append("/usr/local/lib/python2.7/dist-packages")
print (sys.path)

'''''
https://blender.stackexchange.com/questions/8850/how-to-take-images-with-multiple-cameras-with-script?rq=1
https://blender.stackexchange.com/questions/42579/render-depth-map-to-image-with-python-script?rq=1
https://blender.stackexchange.com/questions/14684/how-to-rotate-object-and-render-with-a-script?rq=1
https://blender.stackexchange.com/questions/14941/pixel-coordinates-of-rendered-image-with-python?rq=1

scene = bpy.context.scene

for ob in scene.objects:
    if ob.type == 'CAMERA':
        bpy.context.scene.camera = ob
        print('Set camera %s' % ob.name )
        file = os.path.join("C:/tmp", ob.name )
        bpy.context.scene.render.filepath = file
        bpy.ops.render.render( write_still=True )

'''''

class Parking(object):

  
  sunlight_from = [2]
  sunlight_to = [2]
  blur_from = 0.0
  blur_to = 0.0
  dof = False
  saturation_factor = 1.0
  value_factor = 1.0
  # ranges
  SUNLIGHT_VALUES = [0.01, 0.5, 1.0, 1.5, 2.0, 2.5]

  #define car space top position
  obj_car = []
  #Car_Space_Position_Top=[]

  #func one set Camera paramter，with different rota
  
  Cam_rota=[[[10,0,0],[-9,-13,22]],
            [[20,0,0],[-9,-17,21]],
            [[30,0,0],[-9,-21,19]],
            [[40,0,0],[-9,-23,16]],
            [[50,0,0],[-9,-26,13]],
            #[[60,0,60],[10,-19,10]],
          #[[60,0,75],[10,-19,10]],
          	[[0,0,0],[10,-14,100]],
            #[[60,0,75],[10,-14,10]],
            #[60,0,60]参数表示[pitch，yaw，roll]，[10,-19,10]表示[x,y,z]坐标，改变摄像头的参数从这六个参数修改即可。
            [[70,0,0],[-9,-31,6]],
            [[80,0,0],[-9,-31,6]]
           ]


  def __init__(self,output_dir):

      self.output_dir = output_dir
      #for i in range(np.random.choice(np.arange(Space_Position.shape[0]))-len(bpy.data.objects)):

      
      self.configureBlender()
      self.configureDataset()
      self.setParkingSpots()
      self.AllCarColors()
      self.setCameraPos()
      self.getCarTypesFromBlender()
      
      

      bpy.app.handlers.render_complete.append(self.render_complete)


    
  def startRenderingIteration(self,car_num):
      for j in range(0, car_num): 
      	self.cars = self.getSceneObjects("car")
      	file.write(str(1)+str(self.cars)+"\n")
      	Original_car_medel_num = len(self.Car_classes) 
      	Total_need_car_model_num = np.random.choice(np.arange(3,len(np.array(self.Car_Space_Position_Top).reshape(-1, 3)))) 
      	if Total_need_car_model_num <= Original_car_medel_num:
      		need_car_new_model_num = Total_need_car_model_num
      	else:
      		need_car_new_model_num = Total_need_car_model_num - Original_car_medel_num
      	for n in range(need_car_new_model_num):
      		self.createParkingCars()
      	#file.write(str(self.Car_classes)+"   "+str(Total_need_car_model_num)+ "\n")
      	
      	#file.write(str(len(self.cars))+str(self.cars)+"\n")
      	#file.write(str(self.cars)+"\n")
      	'''
      	print (">>>>>>>99999>>>>>>>>>>")
      	file.write(str(len(self.cars))+"\n")
      	print (">>>>>>>99999>>>>>>>>>>")
      	'''
      	self.cars = self.getSceneObjects("car")
      	file.write(str(2)+str(self.cars)+"\n")
      	#file.write(str(Total_need_car_model_num)+str(len(self.cars))+str(self.cars)+"\n")
      	self.hide_all_cars( )
      	self.sampleCarLocations(Total_need_car_model_num)
      	self.RandomCarColor()
      	self.RandomCarRotation()
      	self.saveLocalImage(j)
      	#bpy.context.scene.render.engine = 'BLENDER_RENDER'
      	bpy.ops.render.render(write_still = True ) 
      	self.RecoveryModel()
      	#bpy.ops.wm.open_mainfile(filepath = "/home/gnss/si/Blender_test/parkinglot/ParkingLot_mini_final_v2.blend")
      	

  def configureBlender(self):
      # rendering constants
      RENDER_RES_X = 640
      RENDER_RES_Y = 480
      FRAME_NO = 10000
      bpy.context.scene.frame_current = FRAME_NO
      bpy.context.scene.render.resolution_x = RENDER_RES_X
      bpy.context.scene.render.resolution_y = RENDER_RES_Y
      bpy.context.scene.render.use_border = False

      self.nodes = bpy.context.scene.node_tree.nodes
      self.links = bpy.context.scene.node_tree.links
      self.nodes['File Output'].base_path = self.output_dir


  def configureDataset(self):
      if not os.path.exists(self.output_dir):
          os.makedirs(self.output_dir)
      if not os.path.exists(self.output_dir + '/images'):
          os.makedirs(self.output_dir + '/images')
      if not os.path.exists(self.output_dir + '/annotations'):
          os.makedirs(self.output_dir + '/annotations')
      if not os.path.exists(self.output_dir + '/prepare'):
          os.makedirs(self.output_dir + '/prepare')




###########################################################################
  def createParkingCars(self): 
      self.createRandomCar()
      print("-----------------  created new object")
      #self.getSceneObjects("car")     

  
  def RecoveryModel(self):
  	bpy.ops.object.select_all(action='DESELECT')#deselect all
  	for car in self.cars:
  		if (car.startswith("car") and ("." in car)):
  			bpy.ops.object.select_pattern(pattern=car)
  			bpy.ops.object.delete(use_global=False)

  		


  def RandomCarColor(self):
  	for carname in self.cars:
  		color = self.colors[np.random.choice(np.arange(len(self.colors)))]
  		color = color.tolist()
  		color.append(1)
  		for slot in bpy.data.objects[carname].material_slots:
  			if (slot.name.startswith("carpaint.Black")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("Carpaint.stainedwhite")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("carpaint_BMW1")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("carpaint_Dodge")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("Carpaint.Blue")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("Carpaint_Golf")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color
  			elif (slot.name.startswith("carpaint_VWT")):
  				nodes = slot.material.node_tree.nodes
  				nodes["Diffuse BSDF"].inputs[0].default_value = color


  def RandomCarRotation(self):
  	for carname in self.cars:
  		if ("car_AudiA8" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_AudiA8"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180
  		elif ("car_BMW335i" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_BMW335i"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180
  		elif ("car_BMWM1" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_BMWM1"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180  	  
  		elif ("car_DodgeRamPickup" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_DodgeRamPickup"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180
  		elif ("car_FIAT" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_FIAT"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180
  		elif ("car_VWGolfMK" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_VWGolfMK"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180
  			bpy.data.objects[carname].scale = bpy.data.objects["car_VWGolfMK"].scale
  		elif ("car_VWTouareg" in carname):
  			bpy.data.objects[carname].rotation_euler = bpy.data.objects["car_VWTouareg"].rotation_euler
  			bpy.data.objects[carname].rotation_euler.z = bpy.data.objects[carname].rotation_euler.z+np.random.choice(np.array([0,math.pi]))+np.random.uniform(-2,2)*math.pi/180  
  
  def hide_all_cars(self):
      for car in self.cars:     
        bpy.data.objects[car].hide_render = True;


  def getCarTypesFromBlender(self):
      self.Car_classes = []
      for obj in bpy.data.objects:  #bpy.context.selected_objects
        if(obj.name.startswith("car") and (not ("." in obj.name))): 
          self.Car_classes.append(obj.name)


  '''
  def showObjects(self):
      for obj in bpy.data.objects:  #bpy.context.selected_objects
        self.obj_car.append(obj)
      
      print(">>>>>000000>>>>>>>")
      print(self.obj_car)
      print (">>>>>00000>>>>>>>>>")


  '''
  def getSceneObjects(self,object_class):
      objects = []
      for obj in bpy.data.objects:  #bpy.context.selected_objects
        #print(obj.name,obj.select)
        if(obj.name.startswith(object_class)):
           objects.append(obj.name)
      #print(object_class ," object :", len(objects))
      print ('>>>>>222222>>>>')
      #print (objects,bpy.data.objects[objects[0]].rotation_euler,objects[0])
      print ('>>>>>222222>>>>')
      return objects



    

  def createRandomCar(self):

      name = np.random.choice(self.Car_classes,1)
      print('createRandomCar',name)
      self.createCarWithName(name[0])

  def createCarWithName(self,name):
      obj = bpy.data.objects[name]
      mesh = obj.data
      new_obj = bpy.data.objects.new(name, mesh)
      bpy.context.scene.objects.link(new_obj)
      new_obj.rotation_mode = 'XYZ'# Force the right rotation mode
      bpy.ops.object.select_all(action='DESELECT')#deselect all
      bpy.ops.object.select_pattern(pattern=new_obj.name)
      bpy.ops.object.make_single_user(object = True, obdata = True, material = True,texture = True )
      '''
      print (">>>>>>>>>>>9999999>>>>>>>>>>>")
      #print (bpy.data.objects["car_AudiA8"].active_material.name,bpy.data.objects[new_obj.name].active_material.diffuse_color)
      print (bpy.context.selected_objects)
      #mat = bpy.data.materials['MatteBlack.001']
      #print (mat.name)
      print (">>>>>>>>>>>9999999>>>>>>>>>>>")
      '''
      


  def AllCarColors(self):
  	self.colors = np.array([
  		[42, 47, 50],[24, 96, 226],[103, 192, 234],[172,65,62],[192,7,22],
  		[42,49,51],[217,216,215],[63,52,58],[22,23,25],[220,115,68],
  		[225,196, 78],[18,71,79],[48,53,91],[194,62,3],[181,107,73],
  		[21,45,69],[176,176,181],[76,74,76],[106,115,146],[142,155,75],
  		[174,218,120],[82, 23, 107],[240,160,149],[55,94,153],[149,194,51],
  		[228,202,81],[230,225,229],[10,10,10]
  		])
  	self.colors = self.colors/255.00

  def setCarLocation(self, car_name, location):
      print( 'arrangeCarLocation', car_name , location  )
      obj = bpy.data.objects[car_name]
      vec = mathutils.Vector((location[0], location[1], 0))
      inv = obj.matrix_world.copy()
      inv.invert()
      vec_rot = vec * inv
      obj.location =vec  #vec_rot 
  
   ############################################################################################   
  def sampleCarLocations(self,n):
      print("car_samples")
      self.Space_Position = np.array(self.Car_Space_Position_Top)
      self.Space_Position = np.array(self.Space_Position).reshape(-1, 3) 
      print(self.Space_Position) 
      random_indices = np.arange(0, self.Space_Position.shape[0])
      print (">>>>>>77777>>>>>")
      print (random_indices)
      np.random.shuffle(random_indices)
      print (random_indices)
      print (">>>>>>77777>>>>>")
      #empty_index = np.where(self.Space_Position[:,2]==0)
      #print( empty_index[0][:n] )
      #print( self.Space_Position[empty_index[0][:n]] )

      cars = self.getSceneObjects("car")
      print (">>>>>>66666>>>>>>")
      #print(cars)
      print (">>>>>>66666>>>>>>")
      car_samples = np.random.choice(cars, n, replace=False)
      print (">>>>>>333333>>>>>>")
      print(car_samples)
      print (n)
      print (">>>>>>33333>>>>>>")

      for i in range(n):
        #print(  car_samples[i], Space_Position[empty_index[0][i]] )
        parking_pos_index = random_indices[i]
        car_name = car_samples[i]
        bpy.data.objects[car_name].hide_render = False;
        car_position = self.Space_Position[parking_pos_index]
        print (">>>>>>>44444>>>>>>>>>>")
        #print (empty_index,car_position)
        print (">>>>>>>44444>>>>>>>>>>")
        self.setCarLocation(car_name, car_position)

  #############################################################################################
  def setParkingSpots(self):
    self.Car_Space_Position_Top=[
         [[-3.24, -11.64, 0],[-5.98, -11.64, 0],[-8.72, -11.64, 0],[-11.46, -11.64, 0],[-14.2, -11.64, 0]],
         [[-3.239,-5.54, 0],[-5.97,-5.54, 0],[-8.71, -5.54, 0],[-11.4, -5.54, 0], [-14.2 ,-5.54, 0]],
         [[14.028,-11.48027,0],[11.29825,-11.3075,0],[8.75127,-11.34205,0],[5.95242,-11.3075,0],[3.39544,-11.34205,0]],
         [[14.00345,-5.77889,0],[11.37736,-5.64068,0],[8.71217,-5.36425,0],[5.98242,-5.3297,0],[3.35633,-5.36425,0]],
         [[-3.72325,-23.53167,0],[-6.43949,-23.38242,0],[-9.17573,-23.53167,0],[-11.76272,-23.53167,0],[-14.29996,-23.43217,0]],
         [[-3.75299,-29.1534,0],[-6.33998,-28.9544,0],[-9.07622,-29.20315,0],[-11.76271,-29.19315,0],[-14.3497,-28.99415,0]],
         [[14.11722,-23.37242,0],[11.23173,-23.52167,0],[8.69449,-23.47192,0],[6.05775,-23.57142,0],[3.37126,-23.52167,0]],
         [[14.11723,-29.29265,0],[11.38099,-29.2429,0],[8.6945,-29.19315,0],[5.96826,-29.4419,0],[3.38127,-29.16315,0]]
        ]

  ################################################################################################    

  def setCameraPos(self):

        cam_ob = bpy.context.scene.camera

        if cam_ob is None:
            print("no scene camera")
        elif cam_ob.type == 'CAMERA':
            print("regular scene cam")
        else:
            print("%s object as camera" % cam_ob.type)

        # https://blender.stackexchange.com/questions/12318/get-position-of-focus-point-of-camera
        # https://stackoverflow.com/questions/42647106/blender-how-to-move-the-camera-from-python-script
        bpy.context.scene.camera.rotation_mode = 'XYZ'
        bpy.data.objects['Camera'].location = self.Cam_rota[5][1]
        bpy.data.objects['Camera'].rotation_euler = [math.radians(self.Cam_rota[5][0][0]+random.random()*0.4), math.radians(0), math.radians(self.Cam_rota[5][0][2]) ]

  def saveLocalImage(self, i):
      filepath = self.output_dir + '/images/' + str(i + 1) + '.png'                            
      bpy.context.scene.render.filepath = filepath
      self.nodes['File Output'].file_slots[0].path = '/images2/'+str(i + 1) 
      


  def render_complete(self, scene):

      print("render complete")
      '''''
      batches = scene.frame_ranges
      i = batches.active_index
      if i < len(batches) - 1:
          batch = batches(i+1)
          # set up scene 
          bpy.ops.render.render('INVOKE_DEFAUT', animation=True)
      else:
          #clear this hander
          bpy.app.handers.render_complete.remove(render_complete)
      '''''

if __name__=="__main__":



    file = open("/home/gnss/Desktop/file.txt","a")
    parking = Parking('/home/gnss/si/Blender_test/parkinglot/Blender_render/({},{})'.format('one', 'two'))
    parking.startRenderingIteration(100)

    '''''
    annot_file = open(output_dir + '/annotations.txt', 'w+')
    annot_file.write('')      
    annot_file.close()
    '''

    
