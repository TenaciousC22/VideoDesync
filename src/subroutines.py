from moviepy.editor import *
import csv
import os
import glob

#Import Silence buffers
def importSilence():
	clips=[]
	clips.append(AudioFileClip("../bin/sound/silence/060.wav"))
	clips.append(AudioFileClip("../bin/sound/silence/240.wav"))
	clips.append(AudioFileClip("../bin/sound/silence/360.wav"))
	return clips

#Creates all offset audio files (+ and - offsets)
#Variables are as follows
#clips: array of clips for padding
#offsets: array of stings of the offsets in milliseconds
#path: file path to audio file you are modifying
#aFile: name of the audio file without the extention
#fType: file extention, include the '.' e.g. ".wav"
def createAudioOffsets(clips, offsets, path, aFile, fType):
	clip=AudioFileClip(path+aFile+fType)
	for i in range(0,len(clips)):
		writePad(clip,clips[i],path,aFile,offsets[i],fType)
		writeCut(clip,path,aFile,offsets[i],fType)
	return

#helper function for createAudioOffsets
def writePad(clip, pad, path, aFile, mod, fType):
	modclip=concatenate_audioclips([pad,clip])
	modclip.write_audiofile(path+aFile+"+"+mod+fType)

#helper function for createAudioOffsets
def writeCut(clip, path, aFile, mod, fType):
	modclip=clip.subclip("00:00:00."+mod)
	modclip.write_audiofile(path+aFile+"-"+mod+fType)

def saveSubclips(vPath, path, fType):
	cPath=os.getcwd()
	intervals=extractIntervals(path)
	vFile=glob.glob(path+"*"+fType)
	vFile=vFile[0]
	for x in range(len(vFile),0,-1):
		if vFile[x-1]=="/":
			vFile=vFile[x:-4]
			break
	print(vFile)
	for x in range(len(intervals)):
		clip=VideoFileClip(path+vFile+fType)
		if x==len(intervals)-1:
			sub=clip.subclip(intervals[x])
		else:
			sub=clip.subclip(intervals[x][0],intervals[x][1])
		os.mkdir(cPath+"/"+vPath+"subclips/"+vFile+str(x+1))
		sub.write_videofile(vPath+"subclips/"+vFile+str(x+1)+"/"+vFile+str(x+1)+fType)

def extractIntervals(path):
	holder=open(path+"intervals.csv","r")
	intervals=[]
	y=0
	for line in holder:
		raw=line
		for x in range(len(raw)):
			if raw[x]==",":
				intervals.append(raw[y:x-1])
				y=x+1
	intervals.append(raw[y:len(raw)-1])
	holder=[]
	for x in range(len(intervals)-1):
		holder.append([intervals[x],intervals[x+1]])
	holder.append(intervals[len(intervals)-1])
	intervals=holder
	return intervals

def createSubclips(vPath, fType):
	fulls=glob.glob(vPath+"full/*")
	saveSubclips(vPath,fulls[0]+"/",fType)
	#print(fulls)