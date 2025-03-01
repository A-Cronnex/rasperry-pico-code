from machine import unique_id

def convert(r,g,b):
    return (255 - r, 255 - g, 255 - b)
def uid():
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())