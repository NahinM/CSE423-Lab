from globData import *
import math

def cam_state():
    if window.cam_state == 0: # First person view
        x, y, z, r = Position.player
        # Camera is on player's head
        cam_z = z + window.wall_heigth  # Place camera at head height
        x2 = x + 200 * math.sin(math.radians(r))
        y2 = y - 200 * math.cos(math.radians(r))
        Position.cam = (x, y, cam_z)
        Position.lookAt = (x2, y2, cam_z)
    elif window.cam_state == 1: #Third person view
        x, y, z, r = Position.player
        # Camera is behind and above the player
        cam_x = x - 250 * math.sin(math.radians(r))
        cam_y = y + 250 * math.cos(math.radians(r))
        cam_z = z + window.wall_heigth + 100  # Slightly above head height
        Position.cam = (cam_x, cam_y, cam_z)
        Position.lookAt = (x, y, z)

