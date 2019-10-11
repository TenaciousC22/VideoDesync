from moviepy.editor import *
from subroutines import *
import csv

#Variables for functions
offsets=["060","240","360"]
clips=importSilence()

if __name__=="__main__":
	#createAudioOffsets(clips, offsets, "../bin/sound/test/", "whiteNoise", ".wav")
	createSubclips("../bin/video/test/", "test", ".mp4")
	#VideoFileClip("../bin/video/test/test.mp4")