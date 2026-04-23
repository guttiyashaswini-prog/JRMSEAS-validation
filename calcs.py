import numpy as np
import json
with open("ldeo.json","r") as f:
    data=json.load()
    model_assumptions=data["model_assumptions"]
    debris_list=data["debris"]
for obj in debris_list:
    mass=obj["mass"]
    shape=obj["shape"]
    dims=obj["dimensions"]
    orbit=obj["orbit"]
    id_=obj["id"]    
    if shape=="box":
        L=dims["length"]
        B=dims["width"]
        H=dims["height"]
        Ixx=(1/12)*mass*(B**2+H**2)
        Iyy=(1/12)*mass*(L**2+H**2)
        Izz=(1/12)*mass*(L**2+B**2)

    elif shape=="cylinder":
        r=dims["radius"]
        h=dims["height"]
        Ixx=Iyy=(1/12)*mass*(3*r**2+h**2)
        Izz=(1/2)*mass*(r**2)

    elif shape=="hollow_cylinder":
        r2=dims["radius"]
        h=dims["height"]
        hollow_ratio=model_assumptions["hollow_ratio"]
        r1=hollow_ratio*r2
        Ixx=Iyy=(1/12)*mass*(3*(r1**2+r2**2)+h**2)
        Izz=(1/2)*mass*(r1**2+r2**2)

    elif shape=="sphere":
        r=dims["radius"]
        Ixx=Iyy=Izz=(2/5)*mass*(r**2)

    else:
        raise ValueError(f"Unknown Shape: {shape}")
    
    I_body=np.array([Ixx,0,0],[0,Iyy,0],[0,0,Izz])

    if shape=="box":
        L=dims["length"]
        B=dims["width"]
        H=dims["height"]
        dx=np.random.uniform(-0.1*L,0.1*L)
        dy=np.random.uniform(-0.1*B,0.1*B)
        dz=np.random.uniform(-0.1*H,0.1*H)

    elif shape=="cylinder":
        r=dims["radius"]
        h=dims["height"]
        dx=np.random.uniform(-0.05*r,0.05*r)
        dy=np.random.uniform(-0.05*r,0.05*r)
        dz=np.random.uniform(-0.1*h,0.1*h)
    elif shape=="hollow_cylinder":
        r=dims["radius"]
        h=dims["height"]
        dx=np.random.uniform(-0.08*r,0.08*r)
        dy=np.random.uniform(-0.08*r,0.08*r)
        dz=np.random.uniform(-0.2*h,0.2*h)

    elif shape=="sphere":
        r=dims["radius"]
        dx=np.random.uniform(-0.01*r,0.01*r)
        dy=np.random.uniform(-0.01*r,0.01*r)
        dz=np.random.uniform(-0.01*r,0.01*r)
    else:
        raise ValueError(f"Unknown Shape: {shape}")
    
d=np.array([dx,dy,dz])
max_dim=max(dims.values())
if np.linalg.norm(d)>0.3*max_dim:
    d=d/np.linalg.norm(d)*0.3*max_dim
I3=np.eye(3)
d_sq=np.dot(d,d)
ddT=np.outer(d,d)
I_shifted=I_body+mass*(d_sq*I3-ddT)