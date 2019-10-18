from moviepy.editor import *
from subroutines import *
import csv

#Variables for functions
offsets=["060","240","360"]
clips=importSilence()
vPath="../bin/video/"
aPath="../bin/sound/"

if __name__=="__main__":
	#createSubclips(vPath, ".mp4")
	offsetAudio(vPath, aPath, offsets, ".mp4")