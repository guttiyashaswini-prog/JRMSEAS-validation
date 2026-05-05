import math

from calcs import Ixx 
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
    percent = float(input("Enter the % of mass assigned to the cylinder (0-100): "))
    print("Enter the coordinates for the lumped mass wrt the COM of the hollow cylinder (meters):")
    xl = float(input("  x: "))
    yl = float(input("  y: "))
    zl = float(input("  z: "))
    results = inertia_tensor_SL16(debris_dict, percent, xl, yl, zl)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")
#________________________________________________________________________________________________
def inertia_tensor_SL16(debris_, per_cy_mass, x_l, y_l, z_l):
    mass = debris_["SL-16"]["mass"]
    height = debris_["SL-16"]["height"]
    diameter = debris_["SL-16"]["diameter"]
    thickness = debris_["SL-16"]["thickness"]
    cy_mass= mass * (per_cy_mass / 100)  # Calculate the mass of the hollow cylinder based on the percentage
    lump_mass = mass - cy_mass  # Calculate the mass of the lumped point mass

    # Calculate the inner and outer radii
    radius_outer = diameter / 2
    radius_inner = radius_outer - thickness

    # Calculate the net COM of the hollow cylinder along with the lumped point mass
    x_com= (x_l*lump_mass)/mass
    y_com= (y_l*lump_mass)/mass
    z_com= (z_l*lump_mass)/mass

    # Calculate the position of the the hollow cylinder COM wrt the new net COM (now origin is shifted to the net COM)
    d_c_x=0-x_com
    d_c_y=0-y_com
    d_c_z=0-z_com

    # Calculate the position of the the lumped point mass COM wrt the new net COM (now origin is shifted to the net COM)
    d_l_x=x_l-x_com
    d_l_y=y_l-y_com
    d_l_z=z_l-z_com

    # Calculate the inertia tensor components for the Entire SL-16 about its own COM(the net COM)
    #EIGENVALUES: Ixx, Iyy, Izz
    Ixx=(1/2)*cy_mass*(radius_outer**2 + radius_inner**2) + (cy_mass*height**2)/12 + lump_mass*(d_l_y**2 + d_l_z**2) + cy_mass*(d_c_y**2 + d_c_z**2)
    Iyy=(1/2)*cy_mass*(radius_outer**2 + radius_inner**2) + (cy_mass*height**2)/12 + lump_mass*(d_l_x**2 + d_l_z**2) + cy_mass*(d_c_x**2 + d_c_z**2)
    Izz=cy_mass*(radius_outer**2 + radius_inner**2) + lump_mass*(d_l_x**2 + d_l_y**2) + cy_mass*(d_c_x**2 + d_c_y**2)

    #Off-diagonal terms (products of inertia)
    Ixy=Iyx= -(lump_mass*d_l_x*d_l_y + cy_mass*d_c_x*d_c_y)
    Ixz=Izx= -(lump_mass*d_l_x*d_l_z + cy_mass*d_c_x*d_c_z)
    Iyz=Izy= -(lump_mass*d_l_y*d_l_z + cy_mass*d_c_y*d_c_z)

    return {"I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}

#*********************ENVISAT INERTIA TENSOR CALCULATION********************
def run_envisat_analysis(debris_dict):
    print("--- ENVISAT Inertia Analysis Tool ---")
    print("Enter the coordinates for the COM of Solar Array wrt the COM of the main bus(Assume that COM is at origin) (meters):")
    xs = float(input("  x: "))
    ys = float(input("  y: "))
    zs = float(input("  z: "))
    print("Enter the coordinates for the COM of ASAR wrt the COM of the main bus(Assume that COM is at origin) (meters):")
    xa = float(input("  x: "))
    ya = float(input("  y: "))
    za = float(input("  z: "))
    results = inertia_tensor_ENVISAT(debris_dict, xs, ys, zs, xa, ya, za)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")
    #______________________________________________________________________________________________
def inertia_tensor_ENVISAT(debris_, x_s, y_s, z_s, x_a, y_a, z_a):
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

    # Calculate the net COM of the entire ENVISAT satellite (now origin is at the net COM)
    x_com= (x_s*sa_mass + x_a*asar_mass)/mass
    y_com= (y_s*sa_mass + y_a*asar_mass)/mass
    z_com= (z_s*sa_mass + z_a*asar_mass)/mass

    # Calculate the position of the Solar Array COM wrt the new net COM (now origin is shifted to the net COM)
    d_s_x=x_s-x_com
    d_s_y=y_s-y_com
    d_s_z=z_s-z_com

    # Calculate the position of the ASAR COM wrt the new net COM (now origin is shifted to the net COM)
    d_a_x=x_a-x_com
    d_a_y=y_a-y_com
    d_a_z=z_a-z_com
    # Calculate the position of the Main Bus COM wrt the new net COM (now origin is shifted to the net COM)
    d_m_x=0-x_com
    d_m_y=0-y_com
    d_m_z=0-z_com
    # Calculate the inertia tensor components for the Entire ENVISAT about its own COM(the net COM)
    #EIGENVALUES: Ixx, Iyy, Izz
    Ixx=(1/12)*sa_mass*(sa_width**2 + sa_height**2) + (1/12)*asar_mass*(asar_width**2 + asar_height**2) + (1/12)*mb_mass*(mb_width**2 + mb_height**2) + sa_mass*(d_s_y**2 + d_s_z**2) + asar_mass*(d_a_y**2 + d_a_z**2) + mb_mass*(d_m_y**2 + d_m_z**2)
    Iyy=(1/12)*sa_mass*(sa_length**2 + sa_height**2) + (1/12)*asar_mass*(asar_length**2 + asar_height**2) + (1/12)*mb_mass*(mb_length**2 + mb_height**2) + sa_mass*(d_s_x**2 + d_s_z**2) + asar_mass*(d_a_x**2 + d_a_z**2) + mb_mass*(d_m_x**2 + d_m_z**2)
    Izz=(1/12)*sa_mass*(sa_length**2 + sa_width**2) + (1/12)*asar_mass*(asar_length**2 + asar_width**2) + (1/12)*mb_mass*(mb_length**2 + mb_width**2) + sa_mass*(d_s_x**2 + d_s_y**2) + asar_mass*(d_a_x**2 + d_a_y**2) + mb_mass*(d_m_x**2 + d_m_y**2)
    
    #Off-diagonal terms (products of inertia)
    Ixy=Iyx= -(sa_mass*d_s_x*d_s_y + asar_mass*d_a_x*d_a_y + mb_mass*d_m_x*d_m_y)
    Ixz=Izx= -(sa_mass*d_s_x*d_s_z + asar_mass*d_a_x*d_a_z + mb_mass*d_m_x*d_m_z)
    Iyz=Izy= -(sa_mass*d_s_y*d_s_z + asar_mass*d_a_y*d_a_z + mb_mass*d_m_y*d_m_z)

    return {"I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}


#IMPORTANT NOTE: Rotational matrices will be added soon. 
# As of now, the COM of all the parts of ENVISAT are assumed to be aligned with the principal axes of the satellite. 
# In reality, this may not be the case and the inertia tensor may need to be rotated to align with the principal axes. 
# *******This will be implemented in a future update.******

#--------------------------------------VESPA INERTIA TENSOR CALCULATION********************
def run_VESPA_analysis(debris_dict):
    results=inertia_tensor_VESPA(debris_dict)
    print("\n--- Calculated Inertia Tensor ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f} kg*m^2")

def inertia_tensor_VESPA(debris_dict):
    mass = debris_dict["VESPA"]["mass"]
    diam_small = debris_dict["VESPA"]["diam_small"]
    diam_large = debris_dict["VESPA"]["diam_large"]
    height = debris_dict["VESPA"]["height"]
    thickness = debris_dict["VESPA"]["thickness"]

    # Calculate the inner and outer radii
    radius_outer_small = diam_small / 2
    radius_outer_large = diam_large / 2
    radius_inner_small = radius_outer_small - thickness
    radius_inner_large = radius_outer_large - thickness

    # Calculate the inertia tensor components for the hollow frustum cone about its COM
    Ixx = (3/10)*mass*((radius_outer_large**5-radius_inner_large**5)/(radius_outer_large**3-radius_inner_large**3) - (radius_outer_small**5-radius_inner_small**5)/(radius_outer_small**3-radius_inner_small**3)) + (3/80)*mass*height**2*((radius_outer_large**4-radius_inner_large**4)/(radius_outer_large**3-radius_inner_large**3) -(radius_outer_small**4-radius_inner_small**4)/(radius_outer_small**3-radius_inner_small**3))
    Iyy = (3/10)*mass*((radius_outer_large**5-radius_inner_large**5)/(radius_outer_large**3-radius_inner_large**3) - (radius_outer_small**5-radius_inner_small**5)/(radius_outer_small**3-radius_inner_small**3)) + (3/80)*mass*height**2*((radius_outer_large**4-radius_inner_large**4)/(radius_outer_large**3-radius_inner_large**3) -(radius_outer_small**4-radius_inner_small**4)/(radius_outer_small**3-radius_inner_small**3))
    Izz = (3/10)*mass*((radius_outer_large**5-radius_inner_large**5)/(radius_outer_large**3-radius_inner_large**3) - (radius_outer_small**5-radius_inner_small**5)/(radius_outer_small**3-radius_inner_small**3))
    Ixy=Iyx=Iyz=Izy=Ixz=Izx=0  # For a frustum cone aligned with the principal axes, the products of inertia are zero

    return {"I_xx": Ixx, "I_yy": Iyy, "I_zz": Izz, "I_xy": Ixy, "I_xz": Ixz, "I_yz": Iyz, "I_yx": Iyx, "I_zx": Izx, "I_zy": Izy}

#IMPORTANT NOTE: The inertia tensor for the VESPA frustum cone is calculated assuming that the there is no asymmetric mass distribution and that the frustum cone is perfectly aligned with the principal axes. 
# In future updates, code will be added for asymmetric mass distribution and for rotating the inertia tensor to align with the principal axes if needed.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------