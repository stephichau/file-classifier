from copy import deepcopy

def make_copy(img):
    return deepcopy(img)

def make_copies(img_array, copies):
    return [make_copy(img) for img in img_array for _ in range(copies)]
