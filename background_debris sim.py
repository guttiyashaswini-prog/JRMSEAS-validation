import numpy as np
import random
import math
class background_deb_sim:
    Orbit="LEO"
    Ref_frame="ECI"
    Background_ID="BGD"
    shape_s=["box","cylinder","sphere","hollow cylinder"]
    debris_info=np.zeros((1200,13))

#***********FRAGMENTATION DEBRIS********************

    for i in range(641):
           debris_info[i,6]=altitude_deb=random.uniform(700,1090)  #kilometers
           debris_info[i,7]=inclinaTion=random.uniform(62,99.5)  #degrees
           debris_info[i,8]=eccentricity=random.uniform(0.0001,0.001)
           FID="F"
           while True:
             UID=random.randint(10000,99999)
             match_found=False
             for j in range(i):
                 if UID==debris_info[j,0]:
                  match_found=True
                  break
             if match_found:
                 continue
             debris_info[i,0]=UID
             break
           JRMSEAS_ID=f"{Background_ID},{FID},{str(UID)}"
           debris_info[i,3]=mass_deb=random.uniform(0.2,500)
           randval=random.randint(1,4)
           if randval==1:
               debris_info[i,3]=density_deb=random.uniform(1100,1400)
           elif randval==2:
               debris_info[i,3]=density_deb=random.uniform(2640,2850)
           elif randval==3:
               debris_info[i,3]=density_deb=random.uniform(4400,4900)
           elif randval==4:
               debris_info[i,3]=density_deb=random.uniform(7600,8960)
           randval1=random.randint(1,4)
           Volume=density_deb/mass_deb
           if randval1==1:
               debris_info[i,4]=shape=shape_s[0,0]
           elif randval1==2:
               debris_info[i,4]=shape=shape_s[0,1]
               radius=None
               hei_var=random.uniform(1.5,4)
               radius=(Volume/(math.pi*(hei_var)))**(1/3)
               height_deb=hei_var*radius
           elif randval1==3:
               debris_info[i,4]=shape=shape_s[0,2]
               radius=((3*Volume)/(4*math.pi))**(1/3)
           elif randval1==4:
               debris_info[i,4]=shape=shape_s[0,3]
               radius1=None
               hei_var=random.uniform(1.5,4)
               rad_var=random.uniform(0.4,0.7)
               radius1=(Volume/(math.pi*hei_var*(1-(rad_var)**2)))**(1/3)
               radius2=rad_var*radius1
               height_deb=hei_var*radius


