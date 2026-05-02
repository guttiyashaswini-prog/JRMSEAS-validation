import math
def box_volume(l,b,h):
    return l*b*h
def cylinder_volume(r,h):
    return math.pi*r**2*h
def hollow_cylinder_volume(r_0uter,r_inner,h):
    return math.pi*h*(r_0uter**2 - r_inner**2)
def object_shape_vol(obj):
    shape=obj['shape']
    dims=obj['dimensions']
    if shape=="box":
        obj['volume']=box_volume(dims['l'],dims['b'],dims['h'])
    elif shape=="cylinder":
        obj['volume']=cylinder_volume(dims['r'],dims['h'])
    elif shape=="hollow_cylinder":
        obj['volume']=hollow_cylinder_volume(dims['r_0uter'],dims['r_inner'],dims['h'])
    if obj['volume']>0:
        obj['density']=obj['mass']/obj['volume']
    else:
        obj['density']=0
    return obj
debris_objects=[
    {
        "name": "Envisat",
        "shape": "box",
        "dimensions": {"l": 26, "b": 10, "h": 5},
        "mass": 8000,
        "volume": 0,
        "density": 0
    },
    {
        "name":"SL-16",
        "shape":"cylinder",
        "dimensions":{"r": 1.95, "h": 9},
        "mass": 9000,
        "volume": 0,
        "density": 0
    },
    {
        "name":"VESPA",
        "shape":"hollow_cylinder",
        "dimensions":{"r_0uter": 2.1, "r_inner": 1.9, "h": 1.3},
        "mass": 113,
        "volume": 0,
        "density": 0
    }
]
processed_data = [object_shape_vol(obj) for obj in debris_objects]
print(f"{'NAME':<12} | {'SHAPE':<16} | {'VOL (m3)':>10} | {'MASS (kg)':>10} | {'DENSITY':>10}")
print("-" * 70)
for obj in processed_data:
    print(f"{obj['name']:<12} | {obj['shape']:<16} | {obj['volume']:>10.2f} | {obj['mass']:>10.1f} | {obj['density']:>10.4f}")
print("\n[SANITY CHECKS]")
max_vol_name = max(processed_data, key=lambda x: x['volume'])['name']
print(f"- Envisat has largest volume: {'PASS' if max_vol_name == 'Envisat' else 'FAIL'}")
min_mass_name = min(processed_data, key=lambda x: x['mass'])['name']
print(f"- VESPA has smallest mass:   {'PASS' if min_mass_name == 'VESPA' else 'FAIL'}")
all_realistic = all(o['density'] < 1000 for o in processed_data)
print(f"- Densities are reasonable:  {'PASS' if all_realistic else 'FAIL'}")