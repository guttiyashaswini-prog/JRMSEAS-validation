import json
import random
def generate_target(i):
    shapes=["box","cylinder","hollow_cylinder"
    ]
    shape=random.choice(shapes)
    if shape=="box":
        dims={
            "x": random.uniform(0,10),
            "y":random.uniform(0,5),
            "z":random.uniform(0,26)
        }