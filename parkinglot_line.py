#coding=utf-8
import sys
import bpy
import math
import random
import colorsys
import os
import mathutils


sys.path.append("/usr/local/lib/python2.7/dist-packages")
print (sys.path)
import png

'''
代码使用全随机方式，生产各种停车场图片
定义了停车场中各组停车位的顶角坐标和相机的相关参数
实际图片生产中，停车场打印的组数由Car_print_team_num控制，
实际打印时只需要更改Car_print_team_num和camera的相关参数即可，位置定义和概率分布等已经比较良好的实现
'''
rot_x = 43
rot_y = 43

# rendering constants
RENDER_RES_X = 640
RENDER_RES_Y = 480
FRAME_NO = 1
car_num = 100
output_dir = '/home/gnss/devdata/si/Parkinglot/parkinglot_line/export_parking_line_10000_160917'
'''
#这些设置的参数都没有使用上
sunlight_from = [2]
sunlight_to = [2]
blur_from = 0.0
blur_to = 0.0
'''
dof = False
saturation_factor = 1.0
value_factor = 1.0

# ranges
SUNLIGHT_VALUES = [0.01, 0.5, 1.0, 1.5, 2.0, 2.5]



if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_dir + '/images'):
    os.makedirs(output_dir + '/images')
if not os.path.exists(output_dir + '/annotations'):
    os.makedirs(output_dir + '/annotations')
if not os.path.exists(output_dir + '/prepare'):
    os.makedirs(output_dir + '/prepare')

bpy.context.scene.frame_current = FRAME_NO

bpy.context.scene.render.resolution_x = RENDER_RES_X
bpy.context.scene.render.resolution_y = RENDER_RES_Y
bpy.context.scene.render.use_border = True

annot_file = open(output_dir + '/annotations.txt', 'w+')
annot_file.write('')



nodes = bpy.context.scene.node_tree.nodes
links = bpy.context.scene.node_tree.links
nodes['File Output'].base_path = output_dir # base_path is Base output path for the image

#define car classes

Car_classes=['AudiA8','AudiA8.001','AudiA8.002','AudiA8.003','AudiA8.004','BMW335i','BMW335i.001',
			 'BMW335i.002','BMW335i.003','BMW335i.004','BMWM1','BMWM1.001','BMWM1.002','BMWM1.003','BMWM1.004',
       'DodgeRamPickup','DodgeRamPickup.001','DodgeRamPickup.002','FIAT500','FIAT500.001','FIAT500.002',
       'FIAT500.003','FIAT500.004','VWGolfMK4.001','VWGolfMK4','VWGolfMK4.002','VWGolfMK4.003','VWGolfMK4.004',
			 'VWTouareg','VWTouareg.001','VWTouareg.002'
			]


#define car space top position
Car_Space_Position_Top=[
      [[-62,29.23],[-49.73,29.23],[-31.82,29.23],[-14.2,29.23],[3.51,29.23],[21.21,29.23],[39.04,29.23],[57.1,29.23]],
      [[-62,11.28],[-49.73,11.28],[-31.82,11.28],[-14.2,11.28],[3.51,11.28],[21.21,11.28] ,[39.04,11.28],[57.1,11.8]],
      [[-62,-5.54],[-49.73,-5.54],[-31.82,-5.54] ,[-14.2,-5.54],[3.51,-5.54],[21.21,-5.54],[39.04,-5.54],[57.1,-5.54]],
      [[-62,-23.1],[-49.73,-23.1],[-31.82,-23.1],[-14.2,-23.1],[3.51,-23.1],[21.21,-23.1],[39.04,-23.1] ,[57.1,-23.1]]
      ]


#func two define ten posi
Car_num_ten_Posi=[
           [-14.2,11.21],[-11.45,11.21],[-8.71,11.21],[-6.2,11.21],[-3.45,11.21],
           [-14.2,5.95],[-11.45,5.95],[-8.71,5.95],[-6.2,5.95],[-3.45,5.95]
        ]


#func one set Camera paramter，with different rota
Cam_rota=[[[10,0,0],[-9,-13,22]],
          [[20,0,0],[-9,-17,21]],
          [[30,0,0],[-9,-21,19]],
          [[40,0,0],[-9,-23,16]],
          [[50,0,0],[-9,-26,13]],
          [[60,0,0],[-9,-27.5,11]],
          [[70,0,0],[-9,-31,6]],
          [[80,0,0],[-9,-31,6]]
         ]


#define car space apart
Car_Space_left_apart_right=2.74
Car_Space_up_apart_down=5.3


#define sapce start posi and car print rows ranks
Car_space_start_posi=[[2,3]]
Car_print_rows=2
Car_print_ranks=5
Car_num_total=Car_print_rows*Car_print_ranks


Car_print_team_num=1
Car_probability=0.8

#get random carSpace satrt position
def getCarSpace_Start_posi(Car_Space_Start_num):
  return random.sample(Car_space_start_posi,Car_Space_Start_num)

#get random CarClasses
def getRandomCarClasses(Car_print_team_num,Car_print_rows,Car_print_ranks):
  return random.sample(Car_classes,Car_print_rows*Car_print_ranks*Car_print_team_num)

#define get sapce position 
def getCarSpace_Position(car_sapce_posi_top_row,car_sapce_posi_top_rank,car_num):
  if car_num<5:
    Car_print_posi=[Car_Space_Position_Top[car_sapce_posi_top_row][car_sapce_posi_top_rank][0]+(car_num)*Car_Space_left_apart_right,Car_Space_Position_Top[car_sapce_posi_top_row][car_sapce_posi_top_rank][1]]
    print(str(Car_print_posi)+'****')
    return Car_print_posi
  else:
    Car_print_posi=[Car_Space_Position_Top[car_sapce_posi_top_row][car_sapce_posi_top_rank][0]+(car_num-5)*Car_Space_left_apart_right,Car_Space_Position_Top[car_sapce_posi_top_row][car_sapce_posi_top_rank][1]-Car_Space_up_apart_down-0.8]
    print(str(Car_print_posi)+'****')
    return Car_print_posi 



#set carSpace empty
def setCarSpace_random_empty(Car_probability):
  Car_weight=10*(1-Car_probability)
  isEmpty=random.randint(0,10)
  if isEmpty>Car_weight:
    isEmpty=1
  else:
    isEmpty=0
  return isEmpty
'''
#主程序中未使用
def get_Ranom_Color():
       r, g, b = [random.random() for i in range(3)]
       return r, g, b	
'''

def hide_all_parkingSpot():
    for parkingSpot in PARKING_CLASSES:
      	bpy.data.objects[parkingSpot].hide_render = True


    

def choose_car_position_byname(name, posi_x,posi_y,posi_z=0,Car_probability=1):    
      if setCarSpace_random_empty(Car_probability)==1:
        bpy.data.objects[name].hide_render = False
        annot_file.write('1 ')
      else:
        print('it did not print\n')
        annot_file.write('0 ')

      vec = mathutils.Vector((posi_x,posi_y, posi_z))
      inv = bpy.data.objects[name].matrix_world.copy() # Worldspace transformation matrix
      inv.invert()
      # vec aligned to local axis
      vec_rot = vec * inv
      #annot_file.write(vec_rot)
      #annot_file.write('\tvec_rot:\t'+str(vec_rot)+'\t')
      bpy.data.objects[name].location = vec
      bpy.data.objects[name].show_bounds = True # Display the object’s bounds
      return bpy.data.objects[name]
              

def hide_all_cars(myCar_classes):
    for car in myCar_classes:
      	bpy.data.objects[car].hide_render = True;

def get_Random_Car(): 

    #value parameter_1:left and right,parameter_2:up and down,parameter_3:high and low
    #bpy.ops.transform.translate(value=(0.0, 0.0, 10.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.0, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), texture_space=False, remove_on_cancel=False, release_confirm=False)
    #set camera center
    #bpy.data.objects['CameraCenter'].rotation_euler = [math.radians(rot_y), 0, math.radians(rot_x)] 
    #annot_file.write(str(bpy.data.materials['Carpaint.stainedwhite'].diffuse_color)+' ')
    #bpy.data.materials['Carpaint.stainedwhite'].diffuse_color=(0,0,0)
    #annot_file.write(str(bpy.data.materials['Carpaint.stainedwhite'].diffuse_color)+' ')

    '''
    annot_file.write(str(bpy.ops.material.copy())+'')
    annot_file.write(str(bpy.ops.object.select_linked(type='MATERIAL'))+' ')
    annot_file.write(str(bpy.data.objects['FIAT500.002'].active_material_index)+' ')
    filepath1 = output_dir + '/images/' + str(i + 1) + '.png'  
    filepath2 = output_dir + '/images2/' + str(i + 1) + '.png'                          
    #bpy.data.objects['CameraCenter'].rotation_euler = [math.radians(rot_y), 0, math.radians(rot_x)]
    print(bpy.data.scenes['Scene'].layers)
    print(bpy.data.objects['Camera'].location,'----------------------\n')
    annot_file.write(str(bpy.data.objects['Camera'].location)+'----------------------\n')
    #print four layers

    choose_car_position_byname('FIAT500.002',-32.02,-23.52)
    bpy.data.scenes['Scene'].layers=[True,True,False,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False]
    bpy.context.scene.render.filepath = filepath1
    bpy.ops.render.render(write_still = True) 
    #print only car layer
    bpy.data.scenes['Scene'].layers=[False,False,False,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False]
    bpy.context.scene.render.filepath = filepath2
    bpy.ops.render.render(write_still = True)   

    annot_file.flush()
	'''
    
	#1.hide all cars
	#2.random get print car num
	#3.random set car space have car or not
	#4.set car in car space
	#5.print picature and print annotation 
    filepath1 = output_dir + '/images/' + str(i+1) + '.png'  
    filepath2 = output_dir + '/images2/' + str(i+1) + '.png'  
    hide_all_cars(Car_classes)
    car_classes_print_list=getRandomCarClasses(Car_print_team_num,Car_print_rows,Car_print_ranks)
    car_space_posi_list=getCarSpace_Start_posi(Car_print_team_num)
    

    annot_file.write(str(filepath1)+'\t')
    #func_1
    
    posi_z=0
    print(str(car_classes_print_list)+'\n'+str(car_space_posi_list)+'\n')
    print(str(car_space_posi_list)+'  '+str(Car_print_rows)+' '+str(Car_print_ranks))
    for car_space_posi_list_len in range(0,len(car_space_posi_list)):
    	for car_posi_print_row_len in range(0,Car_print_rows):
    		for car_posi_print_rank_len in range(0,Car_print_ranks):
    			print('is is '+str(Car_print_rows*Car_print_ranks+car_posi_print_row_len*Car_print_ranks+car_posi_print_rank_len)+'--\n')
    			car_name=car_classes_print_list[Car_print_rows*Car_print_ranks*car_space_posi_list_len+car_posi_print_row_len*Car_print_ranks+car_posi_print_rank_len]
    			car_print_posi=getCarSpace_Position(car_space_posi_list[car_space_posi_list_len][0],car_space_posi_list[car_space_posi_list_len][1],car_posi_print_row_len*Car_print_ranks+car_posi_print_rank_len)
    			#annot_file.write(str(car_name)+' '+str(car_print_posi)+' ')
          #print(str(car_space_posi_list_len)+'  '+str(car_posi_print_row_len)+'  '+str(car_posi_print_rank_len)+'\t'+str(car_space_posi_list_len*Car_print_rows*Car_print_ranks+Car_print_rows*car_posi_print_rank_len+car_posi_print_rank_len)+'  '+str(car_name)+'\n')
    			posi_x=car_print_posi[0]
    			posi_y=car_print_posi[1]
    			choose_car_position_byname(car_name, posi_x,posi_y,posi_z,Car_probability)
          


    '''
    #func_2
    Car_probability=0.8
    for car_posi_num in range(0,10):
      car_name=car_classes_print_list[car_posi_num]
      posi_z=0
      choose_car_position_byname(car_name,Car_num_ten_Posi[car_posi_num][0],Car_num_ten_Posi[car_posi_num][1],posi_z,Car_probability)
      #bpy.data.objects[car_name].location=[Car_num_ten_Posi[0][0],Car_num_ten_Posi[0][1],0]
      annot_file.write('car_name:\t'+car_name+'\t')
    '''

    filepath = output_dir + '/images/' + str(i + 1) + '.png'                            
    bpy.context.scene.render.filepath = filepath          
        
    nodes['File Output'].file_slots[0].path = '/images2/'+str(i + 1) 
    print('Rendering car no. ' + str(i + 1))    

    bpy.ops.render.render(write_still = True)   
    annot_file.write('\n')
    annot_file.flush()







if __name__=="__main__":
	#加载配置文件，摄像头角度距离车辆数目等
    f_parkCon='/home/gnss/mlSoftware/blender-2.76b/data/generator2/generator/parkingline.conf'
    f_parkCon_=open(f_parkCon,'r')
    f_parkCon_lines=f_parkCon_.readlines()
    for f_parkCon_line in f_parkCon_lines:
        f_parkCon_line_=f_parkCon_line.split(':')
        if f_parkCon_line_[0]=='CAMERA_DISTANCE':
            print(f_parkCon_line_[1],'\n')
            CAMERA_DISTANCE=float(f_parkCon_line_[1])
        elif f_parkCon_line_[0]=="rot_x":
            print(f_parkCon_line_[1],'\n')
            rot_x=float(f_parkCon_line_[1])
        elif f_parkCon_line_[0]=="rot_y":
            print(f_parkCon_line_[1],'\n')
            rot_y=float(f_parkCon_line_[1])
        elif f_parkCon_line_[0]=="car_num":
            print(f_parkCon_line_[1],'\n')
            car_num=int(f_parkCon_line_[1])
        else:
            print('\n-------------------- warning')
    #set camera  location
    #bpy.data.objects['Camera'].location = [-9,-24.5, 18]  # x y z
    #bpy.data.objects['Camera'].rotation_euler = [math.radians(50), math.radians(0), math.radians(0)] 
    bpy.data.objects['Camera'].location = Cam_rota[5][1]
    bpy.data.objects['Camera'].rotation_euler = [math.radians(Cam_rota[5][0][0]), math.radians(0), math.radians(0)]

    #for i in range(0, car_num): 
    for i in range(0, car_num): 
      #bpy.data.objects['Camera'].location = Cam_rota[i%8][1]
      #bpy.data.objects['Camera'].rotation_euler = [math.radians(Cam_rota[i%8][0][0]), math.radians(0), math.radians(0)]
      get_Random_Car()
annot_file.close()

#1.bpy.data.objects['Camera'].location = [-18,0 , 75]
#  bpy.data.objects['Camera'].rotation_euler=[math.radians(0),math.radians(0), math.radians(0)]
#2.bpy.data.objects['Camera'].location = [-15,-45, 42]
#  bpy.data.objects['Camera'].rotation_euler=[math.radians(45),math.radians(0), math.radians(0)]
