import math
import numpy as np

#The code is not fully complete and is still being worked on. The code will be updated in the future iterations.
#-----------------------------------------------------------------------------------------
#---------------------------DEBRIS DATA FOR SL-16, ENVISAT, AND VESPA--------------------------------------
debris={
    "SL-16": {  #Zenit-2 SL-16 rocket body
        "mass":9000, #kg
        "shape":"hollow_cylinder", 
        "height": 11.04, #meters
        "diameter": 3.9, #meters
        "thickness": 0.01, #meters
},
     "ENVISAT": {  #ENVISAT satellite
        "mass": 8211, #kg
        "solar array":{
            "mass": 900, #kg
            "shape":"box",
            "length": 14, #meters
            "width": 5, #meters
            "height": 0.02, #meters
        },
          "Main_Bus":{
              "mass": 6494, #kg
              "shape":"box",
            "length": 10.5, #meters
            "width": 4.5, #meters
            "height": 4.5, #meters
        },
        "ASAR":{
            "mass": 817, #kg
            "shape":"box",
            "length": 10, #meters
            "width": 1.3, #meters
            "height": 0.20, #meters
        }},
    "VESPA":{
        "mass": 113, #kg
        "shape":"hollow_frustum_cone",
        "diam_small":1.9, #meters
        "diam_large": 2.1, #meters
        "height":1.3, #meters
        "thickness":0.02 #meters
    }
}
#-----------------------------------------------------------------------------------------
#***************************INERTIA TENSOR CALCULATIONS FOR SL-16, ENVISAT, AND VESPA*******************************
#------------------------------------------------------------------------------------------

#*********************SL-16 INERTIA TENSOR CALCULATION********************
def run_sl16_analysis(debris_dict):
    print("--- SL-16 Inertia Analysis Tool ---")
    percent = float(input("Enter the percentage of mass assigned to the cylinder (0-100): "))
    print("Enter the coordinates for the point lumped mass wrt the geometric center of the hollow cylinder (meters):")
    xl = float(input("  x: "))
    yl = float(input("  y: "))
    zl = float(input("  z: "))
    print("Enter the coordinates for the COM of hollow cylinder wrt the geometric center of the hollow cylinder (meters):")
    xc = float(input("  x: "))
    yc = float(input("  y: "))
    zc = float(input("  z: "))
    # Asking user to input the tilt of the cylinder wrt its COM to calculate inertia
    print("Enter the tilt of the cylinder. (Assume that the COM of cylinder is its local cartesian axis) (in degrees):")
    txc = float(input("  Tilt with x-axis: "))
    tyc = float(input("  Tilt with y-axis: "))
    tzc = float(input("  Tilt with z-axis: "))
    # The tilt of the lumped mass is not asked from the user because it is a pointed mass. 
    results = inertia_tensor_SL16(debris_dict, percent, xl, yl, zl,xc,yc,zc,txc,tyc,tzc)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")
#________________________________________________________________________________________________
def inertia_tensor_SL16(debris_, per_cy_mass, x_l, y_l, z_l,x_c,y_c,z_c,t_xc,t_yc,t_zc):
    mass = debris_["SL-16"]["mass"]
    height = debris_["SL-16"]["height"]
    diameter = debris_["SL-16"]["diameter"]
    thickness = debris_["SL-16"]["thickness"]
    cy_mass= mass * (per_cy_mass / 100)  # Calculate the mass of the hollow cylinder based on the percentage
    lump_mass = mass - cy_mass  # Calculate the mass of the lumped point mass

    # Calculate the inner and outer radii
    radius_outer = diameter / 2
    radius_inner = radius_outer - thickness
    t_radx=math.radians(t_xc)
    t_rady=math.radians(t_yc)
    t_radz=math.radians(t_zc)

    # Calculate the net COM of the hollow cylinder along with the lumped point mass
    x_com= (x_l*lump_mass+x_c*cy_mass)/mass
    y_com= (y_l*lump_mass+y_c*cy_mass)/mass
    z_com= (z_l*lump_mass+z_c*cy_mass)/mass

    # Calculate the position of the the hollow cylinder COM wrt the new net COM (now origin is shifted to the net COM)
    d_c_x=x_c-x_com
    d_c_y=y_c-y_com
    d_c_z=z_c-z_com

    # Calculate the position of the the lumped point mass COM wrt the new net COM (now origin is shifted to the net COM)
    d_l_x=x_l-x_com
    d_l_y=y_l-y_com
    d_l_z=z_l-z_com

    #Calculate cylinder inertia before rotation about its COM.
    Ixx_c=(1/4)*cy_mass*(radius_outer**2 + radius_inner**2) + (cy_mass*height**2)/12
    Iyy_c=(1/4)*cy_mass*(radius_outer**2 + radius_inner**2) + (cy_mass*height**2)/12 
    Izz_c=(1/2)*cy_mass*(radius_outer**2 + radius_inner**2)
    Ixy_c=Iyz_c=Izx_c=Iyx_c=Izy_c=Ixz_c=0
    I_ideal=np.array([[Ixx_c,Ixy_c,Ixz_c],[Iyx_c,Iyy_c,Iyz_c],[Izx_c,Izy_c,Izz_c]])
    
    #Calculate the rotation matrix for the given tilt angles
    R_x=np.array([[1,0,0],[0,math.cos(t_radx),-math.sin(t_radx)],[0,math.sin(t_radx),math.cos(t_radx)]])
    R_y=np.array([[math.cos(t_rady),0,math.sin(t_rady)],[0,1,0],[-math.sin(t_rady),0,math.cos(t_rady)]])
    R_z=np.array([[math.cos(t_radz),-math.sin(t_radz),0],[math.sin(t_radz),math.cos(t_radz),0],[0,0,1]])
    R=R_z @ R_y @ R_x
    I_rotated=R @ I_ideal @ R.T # Calculated the inertia tensor of the cylinder after rotation about its COM.

    # Calculate the inertia tensor components for the Entire SL-16 about its own COM(the net COM)
    #EIGENVALUES: Ixx, Iyy, Izz
    Ixx=I_rotated[0,0] + lump_mass*(d_l_y**2 + d_l_z**2) + cy_mass*(d_c_y**2 + d_c_z**2)
    Iyy=I_rotated[1,1] + lump_mass*(d_l_x**2 + d_l_z**2) + cy_mass*(d_c_x**2 + d_c_z**2)
    Izz=I_rotated[2,2] + lump_mass*(d_l_x**2 + d_l_y**2) + cy_mass*(d_c_x**2 + d_c_y**2)

    #Off-diagonal terms (products of inertia)
    Ixy=Iyx= I_rotated[0,1]-(lump_mass*d_l_x*d_l_y + cy_mass*d_c_x*d_c_y)
    Ixz=Izx= I_rotated[0,2]-(lump_mass*d_l_x*d_l_z + cy_mass*d_c_x*d_c_z)
    Iyz=Izy= I_rotated[1,2]-(lump_mass*d_l_y*d_l_z + cy_mass*d_c_y*d_c_z)

    tensor_matrix = np.array([
        [Ixx, Ixy, Ixz],
        [Iyx, Iyy, Iyz],
        [Izx, Izy, Izz]
    ])
    return {"tensor": tensor_matrix, "I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}

#*********************ENVISAT INERTIA TENSOR CALCULATION********************
def run_envisat_analysis(debris_dict):
    print("--- ENVISAT Inertia Analysis Tool ---")
    print("Enter the coordinates for the COM of Main bus wrt the geometric center of the main bus(meters):")
    xb = float(input("  x: "))
    yb = float(input("  y: "))
    zb = float(input("  z: "))
    print("Enter the coordinates for the COM of Solar Array wrt the geometric center of the main bus(meters):")
    xs = float(input("  x: "))
    ys = float(input("  y: "))
    zs = float(input("  z: "))
    print("Enter the coordinates for the COM of ASAR wrt the geometric center of the main bus (meters):")
    xa = float(input("  x: "))
    ya = float(input("  y: "))
    za = float(input("  z: "))
    print("Enter the tilt of the panel. (Assume that the COM of cylinder is its local cartesian axis) (in degrees):")
    txp = float(input("  Tilt with x-axis: "))
    typ = float(input("  Tilt with y-axis: "))
    tzp = float(input("  Tilt with z-axis: "))
    print("Enter the tilt of the  main bus. (Assume that the COM of cylinder is its local cartesian axis) (in degrees):")
    txm = float(input("  Tilt with x-axis: "))
    tym = float(input("  Tilt with y-axis: "))
    tzm = float(input("  Tilt with z-axis: "))
    print("Enter the tilt of the ASAR. (Assume that the COM of cylinder is its local cartesian axis) (in degrees):")
    txa = float(input("  Tilt with x-axis: "))
    tya = float(input("  Tilt with y-axis: "))
    tza = float(input("  Tilt with z-axis: "))

    results = inertia_tensor_ENVISAT(debris_dict, xs, ys, zs, xa, ya, za,xb,yb,zb, txp, typ, tzp, txm, tym, tzm, txa, tya, tza)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")
    #______________________________________________________________________________________________
def inertia_tensor_ENVISAT(debris_, x_s, y_s, z_s, x_a, y_a, z_a,x_b,y_b,z_b, t_xp, t_yp, t_zp, t_xm, t_ym, t_zm, t_xa, t_ya, t_za):
    mass = debris_["ENVISAT"]["mass"]
        #~~~~~~~~~~~~~~Solar Array parameters~~~~~~~~~~~~~~~~~
    sa_mass = debris_["ENVISAT"]["solar array"]["mass"]
    sa_length = debris_["ENVISAT"]["solar array"]["length"]
    sa_width = debris_["ENVISAT"]["solar array"]["width"]
    sa_height = debris_["ENVISAT"]["solar array"]["height"]
    #~~~~~~~~~~~~~~Main Bus parameters~~~~~~~~~~~~~~~~~
    mb_mass = debris_["ENVISAT"]["Main_Bus"]["mass"]
    mb_length = debris_["ENVISAT"]["Main_Bus"]["length"]
    mb_width = debris_["ENVISAT"]["Main_Bus"]["width"]
    mb_height = debris_["ENVISAT"]["Main_Bus"]["height"]
    #~~~~~~~~~~~~~~ASAR parameters~~~~~~~~~~~~~~~~~
    asar_mass = debris_["ENVISAT"]["ASAR"]["mass"]
    asar_length = debris_["ENVISAT"]["ASAR"]["length"]  
    asar_width = debris_["ENVISAT"]["ASAR"]["width"]
    asar_height = debris_["ENVISAT"]["ASAR"]["height"]

    # Calculate the rotation matrices for the given tilt angles of the solar array, main bus, and ASAR
    # Solar Array rotation matrix
    t_radxp=math.radians(t_xp)
    t_radyp=math.radians(t_yp)
    t_radzp=math.radians(t_zp)
    R_xp=np.array([[1,0,0],[0,math.cos(t_radxp),-math.sin(t_radxp)],[0,math.sin(t_radxp),math.cos(t_radxp)]])
    R_yp=np.array([[math.cos(t_radyp),0,math.sin(t_radyp)],[0,1,0],[-math.sin(t_radyp),0,math.cos(t_radyp)]])
    R_zp=np.array([[math.cos(t_radzp),-math.sin(t_radzp),0],[math.sin(t_radzp),math.cos(t_radzp),0],[0,0,1]])
    R_p=R_zp @ R_yp @ R_xp

    # Main Bus rotation matrix
    t_radxm=math.radians(t_xm)
    t_radym=math.radians(t_ym)
    t_radzm=math.radians(t_zm)
    R_xm=np.array([[1,0,0],[0,math.cos(t_radxm),-math.sin(t_radxm)],[0,math.sin(t_radxm),math.cos(t_radxm)]])
    R_ym=np.array([[math.cos(t_radym),0,math.sin(t_radym)],[0,1,0],[-math.sin(t_radym),0,math.cos(t_radym)]])
    R_zm=np.array([[math.cos(t_radzm),-math.sin(t_radzm),0],[math.sin(t_radzm),math.cos(t_radzm),0],[0,0,1]])
    R_m=R_zm @ R_ym @ R_xm

    # ASAR rotation matrix
    t_radxa=math.radians(t_xa)
    t_radya=math.radians(t_ya)
    t_radza=math.radians(t_za)
    R_xa=np.array([[1,0,0],[0,math.cos(t_radxa),-math.sin(t_radxa)],[0,math.sin(t_radxa),math.cos(t_radxa)]])
    R_ya=np.array([[math.cos(t_radya),0,math.sin(t_radya)],[0,1,0],[-math.sin(t_radya),0,math.cos(t_radya)]])
    R_za=np.array([[math.cos(t_radza),-math.sin(t_radza),0],[math.sin(t_radza),math.cos(t_radza),0],[0,0,1]])
    R_a=R_za @ R_ya @ R_xa

    #Calculate the inertia tensor of the solar array, main bus, and ASAR about their own COMs before rotation
    # Solar Array inertia about its own COM
    Ixxs=(1/12)*sa_mass*(sa_width**2 + sa_height**2)
    Iyys=(1/12)*sa_mass*(sa_length**2 + sa_height**2)
    Izzs=(1/12)*sa_mass*(sa_length**2 + sa_width**2)
    Ixy_s=Ixz_s=Iyz_s=Iyx_s=Izx_s=Izy_s=0
    I_s=np.array([[Ixxs,Ixy_s,Ixz_s],[Iyx_s,Iyys,Iyz_s],[Izx_s,Izy_s,Izzs]])
    I_s_rotated=R_p @ I_s @ R_p.T # Inertia tensor of the solar array after rotation about its own COM

    # Main Bus inertia about its own COM
    Ixxm=(1/12)*mb_mass*(mb_width**2 + mb_height**2)
    Iyym=(1/12)*mb_mass*(mb_length**2 + mb_height**2)
    Izzm=(1/12)*mb_mass*(mb_length**2 + mb_width**2)
    Ixy_m=Ixz_m=Iyz_m=Iyx_m=Izx_m=Izy_m=0
    I_m=np.array([[Ixxm,Ixy_m,Ixz_m],[Iyx_m,Iyym,Iyz_m],[Izx_m,Izy_m,Izzm]])
    I_m_rotated=R_m @ I_m @ R_m.T # Inertia tensor of the main bus after rotation about its own COM

    # ASAR inertia about its own COM
    Ixxa=(1/12)*asar_mass*(asar_width**2 + asar_height**2)
    Iyya=(1/12)*asar_mass*(asar_length**2 + asar_height**2)
    Izza=(1/12)*asar_mass*(asar_length**2 + asar_width**2)
    Ixy_a=Ixz_a=Iyz_a=Iyx_a=Izx_a=Izy_a=0
    I_a=np.array([[Ixxa,Ixy_a,Ixz_a],[Iyx_a,Iyya,Iyz_a],[Izx_a,Izy_a,Izza]])
    I_a_rotated=R_a @ I_a @ R_a.T # Inertia tensor of the ASAR after rotation about its own COM

    # Calculate the net COM of the entire ENVISAT satellite (now origin is at the net COM)
    x_com= (x_s*sa_mass + x_a*asar_mass + x_b*mb_mass)/mass
    y_com= (y_s*sa_mass + y_a*asar_mass + y_b*mb_mass)/mass
    z_com= (z_s*sa_mass + z_a*asar_mass + z_b*mb_mass)/mass

    # Calculate the position of the Solar Array COM wrt the new net COM (now origin is shifted to the net COM)
    d_s_x=x_s-x_com
    d_s_y=y_s-y_com
    d_s_z=z_s-z_com
    # Calculate the position of the ASAR COM wrt the new net COM (now origin is shifted to the net COM)
    d_a_x=x_a-x_com
    d_a_y=y_a-y_com
    d_a_z=z_a-z_com
    # Calculate the position of the Main Bus COM wrt the new net COM (now origin is shifted to the net COM)
    d_m_x=x_b-x_com
    d_m_y=y_b-y_com
    d_m_z=z_b-z_com

    # Calculate the inertia tensor components for the Entire ENVISAT about its own COM(the net COM)
    #EIGENVALUES: Ixx, Iyy, Izz
    Ixx=I_a_rotated[0,0] + I_s_rotated[0,0] + I_m_rotated[0,0] + sa_mass*(d_s_y**2 + d_s_z**2) + asar_mass*(d_a_y**2 + d_a_z**2) + mb_mass*(d_m_y**2 + d_m_z**2)
    Iyy=I_a_rotated[1,1] + I_s_rotated[1,1] + I_m_rotated[1,1] + sa_mass*(d_s_x**2 + d_s_z**2) + asar_mass*(d_a_x**2 + d_a_z**2) + mb_mass*(d_m_x**2 + d_m_z**2)
    Izz=I_a_rotated[2,2] + I_s_rotated[2,2] + I_m_rotated[2,2] + sa_mass*(d_s_x**2 + d_s_y**2) + asar_mass*(d_a_x**2 + d_a_y**2) + mb_mass*(d_m_x**2 + d_m_y**2)

    #Off-diagonal terms (products of inertia)
    Ixy=Iyx= I_s_rotated[0,1] + I_a_rotated[0,1] + I_m_rotated[0,1] - (sa_mass*d_s_x*d_s_y + asar_mass*d_a_x*d_a_y + mb_mass*d_m_x*d_m_y)
    Ixz=Izx= I_s_rotated[0,2] + I_a_rotated[0,2] + I_m_rotated[0,2] - (sa_mass*d_s_x*d_s_z + asar_mass*d_a_x*d_a_z + mb_mass*d_m_x*d_m_z)
    Iyz=Izy= I_s_rotated[1,2] + I_a_rotated[1,2] + I_m_rotated[1,2] - (sa_mass*d_s_y*d_s_z + asar_mass*d_a_y*d_a_z + mb_mass*d_m_y*d_m_z)

    return {"I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}

#IMPORTANT NOTE: As of now, the code assumes that the solar array follows rigid body dynamics and does not account for the flexibility of the solar array. 
# This is a simplification and may not be accurate for real-world scenarios. 
# Future iterations of the code will include the effects of solar array flexibility on the inertia tensor calculation.

#--------------------------------------VESPA INERTIA TENSOR CALCULATION********************
def run_VESPA_analysis(debris_dict):
    print("Enter the coordinates for the COM offset of VESPA(assume it to be a hollow thin conical frustum) wrt the COM without any offsets (meters):")
    xv = float(input("  x: "))
    yv = float(input("  y: "))
    zv = float(input("  z: "))
    print("Enter the tilt of the VESPA (consider the offset com as its origin) (in degrees):")
    txv = float(input("  Tilt with x-axis: "))
    tyv = float(input("  Tilt with y-axis: "))
    tzv = float(input("  Tilt with z-axis: "))
    results=inertia_tensor_VESPA(debris_dict,xv,yv,zv,txv,tyv,tzv)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")

def inertia_tensor_VESPA(debris_dict,x_v,y_v,z_v,tx_v,ty_v,tz_v):
    mass = debris_dict["VESPA"]["mass"]
    diam_small = debris_dict["VESPA"]["diam_small"]
    diam_large = debris_dict["VESPA"]["diam_large"]
    height = debris_dict["VESPA"]["height"]
    thickness = debris_dict["VESPA"]["thickness"]

    # Calculate the inner and outer radii
    radius_outer_small = diam_small / 2
    radius_outer_large = diam_large / 2
    radius_small_avg = radius_outer_small - thickness/2
    radius_large_avg = radius_outer_large - thickness/2

    # Calculate the inertia tensor components for the hollow frustum cone about its COM(without offsets)
    Ixx_id = 0.25*mass*(radius_small_avg**2+radius_large_avg**2)+(mass/18)*height**2*((radius_large_avg**2+radius_small_avg**2+radius_small_avg*radius_large_avg)/(radius_large_avg+radius_small_avg)**2)
    Iyy_id = 0.25*mass*(radius_small_avg**2+radius_large_avg**2)+(mass/18)*height**2*((radius_large_avg**2+radius_small_avg**2+radius_small_avg*radius_large_avg)/(radius_large_avg+radius_small_avg)**2)
    Izz_id = 0.5*mass*(radius_small_avg**2+radius_large_avg**2)

    # Calculate the rotation matrices for the given tilt angles of the VESPA
    t_radx=math.radians(tx_v)
    t_rady=math.radians(ty_v)
    t_radz=math.radians(tz_v)
    R_x=np.array([[1,0,0],[0,math.cos(t_radx),-math.sin(t_radx)],[0,math.sin(t_radx),math.cos(t_radx)]])
    R_y=np.array([[math.cos(t_rady),0,math.sin(t_rady)],[0,1,0],[-math.sin(t_rady),0,math.cos(t_rady)]])
    R_z=np.array([[math.cos(t_radz),-math.sin(t_radz),0],[math.sin(t_radz),math.cos(t_radz),0],[0,0,1]])
    R=R_z @ R_y @ R_x
    I_rotated=R @ np.array([[Ixx_id,0,0],[0,Iyy_id,0],[0,0,Izz_id]]) @ R.T # Inertia tensor of the VESPA after rotation about its COM without offsets.

    # Calculate the change in tensor after COM offset
    # the eigenvalues
    Ixx_of=mass*(y_v**2+z_v**2)
    Iyy_of=mass*(x_v**2+z_v**2)
    Izz_of=mass*(x_v**2+y_v**2)
    # Final off diagonal tensors
    Ixy=Iyx=I_rotated[0,1]-(mass*x_v*y_v)
    Iyz=Izy=I_rotated[1,2]-(mass*y_v*z_v)
    Izx=Ixz=I_rotated[2,0]-(mass*z_v*x_v)

# Final eigenvalues
    Ixx=I_rotated[0,0]+Ixx_of
    Iyy=I_rotated[1,1]+Iyy_of
    Izz=I_rotated[2,2]+Izz_of

# Added code for asymmetric mass distribution
# Offset COM can lead to asymmetric mass distribution which can cause the products of inertia to be non-zero.

    return {"I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------