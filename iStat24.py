#!/usr/bin/python

import json, requests, pprint, time
import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.minecraftstuff as minecraftstuff

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
    
data = requests.get("https://istat24.com.ua/api/efabce790ad19efb0fbe3879af252144/calls.json?counter_start_date=2016-02-01&counter_end_date=2016-02-05")
json = json.loads(data.content)

mc = minecraft.Minecraft.create()
mcdrawing = minecraftstuff.MinecraftDrawing(mc)
	
def drawCall(x, y, z, length, blockType):
	length = (length, 200)[length>200]
	for i in range(y, y+length):
		mc.setBlock(x, i, z, blockType)
		mc.setBlock(x+1, i, z, blockType)
		mc.setBlock(x+1, i, z+1, blockType)
		mc.setBlock(x, i, z+1, blockType)
						
pos = mc.player.getTilePos()

mc.postToChat("START")
mc.postToChat("USER Position: x="+str(pos.x) + " y=" + str(pos.y) + " z=" + str(pos.z))	

startX=146; startY=0; startZ=-30

# Clean up
mc.setBlocks(startX-2, startY-20, startZ+5, startX+2, startY+200, startZ-250, 8)
time.sleep(2)
mc.setBlocks(startX-3, startY-1, startZ+6, startX+3, startY+210, startZ-551, block.AIR.id)
time.sleep(2)

# cleanUp(pos.x, pos.y, pos.z, 40) # Clean up self
mc.postToChat("Clean up is done")

offset=0
for call in json:
	offset+=3
	duration = get_sec(call['duration'])
	wait_duration = get_sec(call['wait_duration'])
	speak_duration = get_sec(call['speak_duration'])	
	
	if call['accepted'] == 1:
# 		print duration, height
		drawCall(startX, startY, startZ-offset, wait_duration, 41) # wait_duration
		drawCall(startX, startY+wait_duration, startZ-offset, speak_duration, 133) #speak_duration
	else:		 
		drawCall(startX, startY, startZ-offset, duration, 152) # duration


mc.postToChat("DONE")

