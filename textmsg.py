__author__ = 'justin'

msg = {
    "health": "Health Collected",
    "ammo": "Ammunition Collected",
    "rocketitem": "Rocket Launcher Obtained",
    "rockets":"Rockets Obtained",
    "dual": "Dual Rail Gun Attachment Obtained",
    "damage": "Damage Taken",
    "speed": "Speed",
    "spread": "Wide Shot Canon Obtained",
    "orb": "Shield"
}

weapons = {
    "rocketitem": "Rocket Launcher Obtained",
    "dual": "Dual Rail Gun Attachment Obtained",
    "spread": "Wide Shot Canon Obtained"
}

#def non_weapon(type, amount):
    #return
non_weapon = lambda type, amount: str(amount)+ "+" + " " + msg[type]
weapon = lambda type: weapons[type]
rocket_ammo = lambda amount: str(amount) + "+" + " " + msg["rockets"]
take_damage = lambda amount: str(amount) + " " + msg["damage"]