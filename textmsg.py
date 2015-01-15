__author__ = 'justin'

msg = {
    "health": "Health Collected",
    "ammo": "Ammo Collect",
    "rocketitem": "Rocket Launcher Obtained",
    "dual": "Dual Gun Attachment Obtained"
}

def non_weapon(type,amount):
    return str(amount)+ "+" + " " + msg[type]


