from moviepy.editor import *
from moviepy import *
from subroutines import *
import csv
import cv2
import numpy as np

#Variables for functions
offsets=["060","240","360","480","600","720","840"]
clips=importSilence()
vPath="..\\bin\\video\\"
aPath="..\\bin\\sound\\"

if __name__=="__main__":
	#convertToMP4(vPath)
	#addFixedAudio(vPath)
	#createSubclips(vPath, ".mp4")
	#offsetAudio(vPath, aPath, offsets, ".mp4")
	#jumble(vPath)

	#balanceBabble()
	addNoiseAndDownSample(vPath,"-7DbBabble.wav",offsets,".mp4")

	convertToMono(vPath,offsets,".mp4")
	#clip=VideoFileClip("../bin/video/subclips/test1/test1.mp4")
	#clip1=VideoFileClip("../bin/video/subclips/test1/test1+360.mp4")
	#clip2=VideoFileClip("../bin/video/subclips/test1/test1-360.mp4")
	#clip.preview()