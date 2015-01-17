__author__ = 'justin'

msg = {
    "health": "Health Collected",
    "ammo": "Ammo Collected",
    "rocketitem": "Rocket Launcher Obtained",
    "rockets":"Rockets Obtained",
    "dual": "Dual Gun Attachment Obtained",
    "damage": "Damage Taken"
}

#def non_weapon(type, amount):
    #return
non_weapon = lambda type, amount: str(amount)+ "+" + " " + msg[type]
rocket_ammo = lambda amount: str(amount) + "+" + " " + msg["rockets"]
take_damage = lambda amount: str(amount) + " " + msg["damage"]