import numpy as np
import random
import math
import pandas as pd

Orbit="LEO"
Ref_frame="ECI"
Background_ID="BGD"
shape_s=["box","cylinder","sphere","hollow cylinder"]
GM=3.986*10**14  #m^3/s^2
R_earth=6371000  #meters
jrmseas_debrisDatabase=[]
used_uids = set() 
def generate_uid(used_uids):
    while True:
        uid = random.randint(10000,99999)
        if uid not in used_uids:
            used_uids.add(uid)
            return uid
def generate_orbit():
    altitude_deb = random.uniform(700,1090)
    inclination = random.uniform(62,99.5)
    eccentricity = random.uniform(0.0001,0.001)
    d_earth_debris = R_earth + altitude_deb*1000
    semi_major_axis = d_earth_debris/(1-eccentricity)

    return altitude_deb, inclination, eccentricity, semi_major_axis
def generate_shape_and_motion(Volume, GM, eccentricity, semi_major_axis, shape_s, allow_rotation=True):
    
    length_deb = breadth_deb = height_deb = None
    radius1 = radius2 = None
    randval1 = random.randint(1,4)
    v_min = ((GM*(1-eccentricity))/(semi_major_axis*(1+eccentricity)))**0.5
    v_max = ((GM*(1+eccentricity))/(semi_major_axis*(1-eccentricity)))**0.5
    # ---------------- BOX ---------------------------------------------------------
    if randval1 == 1:
        shape = shape_s[0]
        length_const = random.uniform(1.5,4)
        breadth_const = random.uniform(1.5,4)
        height_const = random.uniform(1.5,4)

        base_dim = (Volume/(length_const*breadth_const*height_const))**(1/3)

        length_deb = length_const * base_dim
        breadth_deb = breadth_const * base_dim
        height_deb = height_const * base_dim

        small = (length_deb < 1 and breadth_deb < 1 and height_deb < 1)
        can_rotate = allow_rotation and (not small)
        rotational_vel = 0 if not can_rotate else random.uniform(3,60)
        translational_vel = random.uniform(v_min, v_max)

        comoffset_x = np.random.uniform(-0.1*length_deb,0.1*length_deb)
        comoffset_y = np.random.uniform(-0.1*breadth_deb,0.1*breadth_deb)
        comoffset_z = np.random.uniform(-0.1*height_deb,0.1*height_deb)

    # ---------------- CYLINDER ----------------
    elif randval1 == 2:
        shape = shape_s[1]

        hei_var = random.uniform(1.5,4)
        radius1 = (Volume/(math.pi*(hei_var)))**(1/3)
        height_deb = hei_var * radius1

        small = (height_deb < 1 and radius1 < 1)
        can_rotate = allow_rotation and (not small)
        rotational_vel = 0 if not can_rotate else random.uniform(3,60)
        translational_vel = random.uniform(v_min, v_max)

        comoffset_x = np.random.uniform(-0.05*radius1,0.05*radius1)
        comoffset_y = np.random.uniform(-0.05*radius1,0.05*radius1)
        comoffset_z = np.random.uniform(-0.1*height_deb,0.1*height_deb)

    # ---------------- SPHERE ----------------
    elif randval1 == 3:
        shape = shape_s[2]

        radius1 = ((3*Volume)/(4*math.pi))**(1/3)

        small = (radius1 < 1)
        can_rotate = allow_rotation and (not small)
        rotational_vel = 0 if not can_rotate else random.uniform(3,60)
        translational_vel = random.uniform(v_min, v_max)

        comoffset_x = np.random.uniform(-0.01*radius1,0.01*radius1)
        comoffset_y = np.random.uniform(-0.01*radius1,0.01*radius1)
        comoffset_z = np.random.uniform(-0.01*radius1,0.01*radius1)

    # ---------------- HOLLOW CYLINDER ----------------
    else:
        shape = shape_s[3]

        hei_var = random.uniform(1.5,4)
        rad_var = random.uniform(0.4,0.7)

        radius1 = (Volume/(math.pi*hei_var*(1-(rad_var)**2)))**(1/3)
        radius2 = rad_var * radius1
        height_deb = hei_var * radius1

        small = (height_deb < 1 and radius1 < 1 and radius2 < 1)
        can_rotate = allow_rotation and (not small)

        rotational_vel = 0 if not can_rotate else random.uniform(3,60)
        translational_vel = random.uniform(v_min, v_max)

        comoffset_x = np.random.uniform(-0.08*radius1,0.08*radius1)
        comoffset_y = np.random.uniform(-0.08*radius2,0.08*radius2)
        comoffset_z = np.random.uniform(-0.2*height_deb,0.2*height_deb)

    return (
        shape,
        length_deb, breadth_deb, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    )
def generate_rocket_body(Volume, GM, eccentricity, semi_major_axis):
    shape = "hollow cylinder"
    height_deb = random.uniform(10, 40)   
    thickness_ratio = random.uniform(0.02, 0.1)  
    t = thickness_ratio
    radius1 = (Volume / (math.pi * height_deb * (1 - (1 - t)**2)))**0.5
    radius1 = min(radius1, height_deb / 2)
    radius2 = (1 - t) * radius1
    v_min = ((GM*(1-eccentricity))/(semi_major_axis*(1+eccentricity)))**0.5
    v_max = ((GM*(1+eccentricity))/(semi_major_axis*(1-eccentricity)))**0.5   
    translational_vel = random.uniform(v_min, v_max)
    rotational_vel = random.uniform(0.01, 2)
    comoffset_x = np.random.uniform(-0.08*radius1, 0.08*radius1)
    comoffset_y = np.random.uniform(-0.08*radius2, 0.08*radius2)
    comoffset_z = np.random.uniform(-0.2*height_deb, 0.2*height_deb)
    return (
        shape,
        None, None, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    )
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#*********************FRAGMENTATION DEBRIS**************************
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
for i in range(640):

    altitude, inclination, eccentricity, semi_major_axis = generate_orbit()
    FID = "F"
    UID = generate_uid(used_uids)
    JRMSEAS_ID = f"{Background_ID}{FID}{UID}"
    mass_deb = random.uniform(0.2,500)
    randval = random.randint(1,4)
    if randval==1:
        density_deb=random.uniform(1100,1400)
    elif randval==2:
        density_deb=random.uniform(2640,2850)
    elif randval==3:
        density_deb=random.uniform(4400,4900)
    else:
        density_deb=random.uniform(7600,8960)
    Volume = mass_deb / density_deb
    (
        shape,
        length_deb, breadth_deb, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    ) = generate_shape_and_motion(
        Volume, GM, eccentricity, semi_major_axis, shape_s
    )
    row = {
        'Index': i,
        'Unique ID': UID,
        'JRMSEAS_ID': JRMSEAS_ID,
        'Shape': shape,
        'Mass': mass_deb,
        'Density': density_deb,
        'L': length_deb,
        'W': breadth_deb,
        'H': height_deb,
        'R1': radius1,
        'R2': radius2,
        'Inclination': inclination,
        'Eccentricity': eccentricity,
        'Alt_km': altitude,  
        'V_trans': translational_vel,
        'V_rot': rotational_vel,
        'CoM_X': comoffset_x,
        'CoM_Y': comoffset_y,
        'CoM_Z': comoffset_z
    }

    jrmseas_debrisDatabase.append(row)
#----------------------------------------------------------------------------------------------
#******************************MISSION RELATED DEBRIS******************************************
#----------------------------------------------------------------------------------------------
   
for i in range(640,820):
    altitude, inclination, eccentricity, semi_major_axis = generate_orbit()
    FID = "M"
    UID = generate_uid(used_uids)
    JRMSEAS_ID = f"{Background_ID}{FID}{UID}"
    mass_deb = random.uniform(5, 100)
    density_deb=random.uniform(2500,5000)
    Volume = mass_deb / density_deb
    (
        shape,
        length_deb, breadth_deb, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    ) = generate_shape_and_motion(
        Volume, GM, eccentricity, semi_major_axis, shape_s
    )
    row = {
        'Index': i,
        'Unique ID': UID,
        'JRMSEAS_ID': JRMSEAS_ID,
        'Shape': shape,
        'Mass': mass_deb,
        'Density': density_deb,
        'L': length_deb,
        'W': breadth_deb,
        'H': height_deb,
        'R1': radius1,
        'R2': radius2,
        'Inclination': inclination,
        'Eccentricity': eccentricity,
        'Alt_km': altitude,
        'V_trans': translational_vel,
        'V_rot': rotational_vel,
        'CoM_X': comoffset_x,
        'CoM_Y': comoffset_y,
        'CoM_Z': comoffset_z
    }

    jrmseas_debrisDatabase.append(row)
    
#-------------------------------------------------------------------------------------------------------------------------
#**************************DEFUNCT SATELLITES*********************************************
#--------------------------------------------------------------------------------------------------------
    
for i in range(820,920):
    altitude, inclination, eccentricity, semi_major_axis = generate_orbit()
    FID = "D"
    UID = generate_uid(used_uids)
    JRMSEAS_ID = f"{Background_ID}{FID}{UID}"
    mass_deb = random.uniform(20, 8000)
    density_deb=random.uniform(2500,5000)
    Volume = mass_deb / density_deb
    (
        shape,
        length_deb, breadth_deb, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    ) = generate_shape_and_motion(
        Volume, GM, eccentricity, semi_major_axis, shape_s
    )
    row = {
        'Index': i,
        'Unique ID': UID,
        'JRMSEAS_ID': JRMSEAS_ID,
        'Shape': shape,
        'Mass': mass_deb,
        'Density': density_deb,
        'L': length_deb,
        'W': breadth_deb,
        'H': height_deb,
        'R1': radius1,
        'R2': radius2,
        'Inclination': inclination,
        'Eccentricity': eccentricity,
        'Alt_km': altitude,
        'V_trans': translational_vel,
        'V_rot': rotational_vel,
        'CoM_X': comoffset_x,
        'CoM_Y': comoffset_y,
        'CoM_Z': comoffset_z
    }

    jrmseas_debrisDatabase.append(row)

#------------------------------------------------------------------------------------------
#*****************************ROCKET BODY***********************************
#----------------------------------------------------------------------------------

for i in range(920,1000):
    altitude, inclination, eccentricity, semi_major_axis = generate_orbit()
    FID = "R"
    UID = generate_uid(used_uids)
    JRMSEAS_ID = f"{Background_ID}{FID}{UID}"
    mass_deb = random.uniform(1000, 9000)
    density_deb=random.uniform(1500,3000)
    Volume = mass_deb / density_deb
    (
    shape,
    length_deb, breadth_deb, height_deb,
    radius1, radius2,
    translational_vel, rotational_vel,
    comoffset_x, comoffset_y, comoffset_z
) = generate_rocket_body(
    Volume, GM, eccentricity, semi_major_axis
)
    row = {
        'Index': i,
        'Unique ID': UID,
        'JRMSEAS_ID': JRMSEAS_ID,
        'Shape': shape,
        'Mass': mass_deb,
        'Density': density_deb,
        'L': length_deb,
        'W': breadth_deb,
        'H': height_deb,
        'R1': radius1,
        'R2': radius2,
        'Inclination': inclination,
        'Eccentricity': eccentricity,
        'Alt_km': altitude,
        'V_trans': translational_vel,
        'V_rot': rotational_vel,
        'CoM_X': comoffset_x,
        'CoM_Y': comoffset_y,
        'CoM_Z': comoffset_z
    }

    jrmseas_debrisDatabase.append(row)

#----------------------------------------------------------------------------------------
#**********************SURFACE EROSION PARTICLES*********************************************
#----------------------------------------------------------------------------------------
    
for i in range(1000,1200):
    altitude, inclination, eccentricity, semi_major_axis = generate_orbit()
    FID = "S"
    UID = generate_uid(used_uids)
    JRMSEAS_ID = f"{Background_ID}{FID}{UID}"
    mass_deb = random.uniform(0.001,0.01)
    density_deb = random.uniform(900,2500)
    Volume = mass_deb / density_deb
    (
        shape,
        length_deb, breadth_deb, height_deb,
        radius1, radius2,
        translational_vel, rotational_vel,
        comoffset_x, comoffset_y, comoffset_z
    ) = generate_shape_and_motion(
        Volume,
        GM,
        eccentricity,
        semi_major_axis,
        shape_s,
        allow_rotation=False  
    )
    row = {
        'Index': i,
        'Unique ID': UID,
        'JRMSEAS_ID': JRMSEAS_ID,
        'Shape': shape,
        'Mass': mass_deb,
        'Density': density_deb,
        'L': length_deb,
        'W': breadth_deb,
        'H': height_deb,
        'R1': radius1,
        'R2': radius2,
        'Inclination': inclination,
        'Eccentricity': eccentricity,
        'Alt_km': altitude,
        'V_trans': translational_vel,
        'V_rot': rotational_vel,   # will be 0 automatically
        'CoM_X': comoffset_x,
        'CoM_Y': comoffset_y,
        'CoM_Z': comoffset_z
    }
    jrmseas_debrisDatabase.append(row)

df=pd.DataFrame(jrmseas_debrisDatabase)
df.to_csv("JRMSEAS_Debris_Catalog.csv", index=False)