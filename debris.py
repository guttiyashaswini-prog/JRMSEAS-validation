import math
import copy
# Units: SI (meters, kilograms, cubic meters)
def box_volume(l,b,h):
    return l*b*h
def cylinder_volume(r,h):
    return math.pi*r**2*h
def hollow_cylinder_volume(r_outer,r_inner,h):
    if r_outer <= r_inner:
        raise ValueError(f"Outer radius ({r_outer}) must be greater than inner radius ({r_inner})")
    return math.pi*h*(r_outer**2 - r_inner**2)
def validate_dimensions(shape, dims):
    required_keys = {
        "box": ["l", "b", "h"],
        "cylinder": ["r", "h"],
        "hollow_cylinder": ["r_outer", "r_inner", "h"]
    }
    if shape not in required_keys:
        raise ValueError(f"Unexpected shape received: {shape}")
    for key in required_keys[shape]:
        if key not in dims:
            raise ValueError(f"Missing dimension '{key}' for shape '{shape}'")
        if dims[key] <= 0:
            raise ValueError(f"[ERROR] Invalid value for '{key}' in '{shape}': must be > 0")
    return True
def process_object(original_obj):
    """Returns a NEW object with calculated metrics to avoid mutation."""
    obj = copy.deepcopy(original_obj) 
    shape = obj['shape']
    dims = obj['dimensions']
    
    validate_dimensions(shape, dims)
    if shape=="box":
        obj['volume']=box_volume(dims['l'],dims['b'],dims['h'])
    elif shape=="cylinder":
        obj['volume']=cylinder_volume(dims['r'],dims['h'])
    elif shape=="hollow_cylinder":
        obj['volume']=hollow_cylinder_volume(dims['r_outer'],dims['r_inner'],dims['h'])
    else:
        raise ValueError(f"Unexpected shape '{shape}' in object '{obj['name']}'")
    if obj['volume'] <= 0:
        raise ValueError(f"[ERROR] Non-physical volume for '{obj['name']}'")
    obj['density'] = obj['mass'] / obj['volume']
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
        "dimensions":{"r_outer": 2.1, "r_inner": 1.9, "h": 1.3},
        "mass": 113,
        "volume": 0,
        "density": 0
    }
]
processed_data = [process_object(obj) for obj in debris_objects]
densest = max(processed_data, key=lambda x: x['density'])
least_dense = min(processed_data, key=lambda x: x['density'])
print(f"{'NAME':<12} | {'VOL (m3)':>10} | {'DENSITY (kg/m3)':>15}")
print("-" * 45)
for obj in processed_data:
    print(f"{obj['name']:<12} | {obj['volume']:>10.2f} | {obj['density']:>15.4f}")
print("\n[RESEARCH INSIGHTS]")
physically_plausible = all(0.1 < o['density'] < 22600 for o in processed_data)
print(f"- Materials are physically plausible: {'PASS' if physically_plausible else 'FAIL'}")

print(f"- Highest Density: {densest['name']} ({densest['density']:.2f} kg/m3)")
print(f"  REASON: Rocket bodies (SL-16) feature concentrated steel/alloy structures and engine clusters.")
print(f"- Lowest Density:  {least_dense['name']} ({least_dense['density']:.2f} kg/m3)")
print(f"  REASON: Satellites (Envisat) or Adapters (VESPA) are high-volume shells with vast internal voids.")

print("\n[MODEL LIMITATIONS & UNCERTAINTIES]")
print("1. NON-UNIFORMITY: This model assumes uniform density. In reality, mass is clustered in")
print("   engines. Center of Mass (CoM) likely deviates significantly from geometric center.")
print("2. STRUCTURAL VOIDS: 'Volume' here is the total bounding envelope. For objects like Envisat,")
print("   internal voids dominate, explaining the lower compared to compact structures.")
print("3. RADIATIVE PRESSURE: Objects with low density (high Area-to-Mass ratio) like Envisat or")
print("   VESPA are more susceptible to orbital perturbations from Solar Radiation Pressure.")