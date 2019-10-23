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
		if len(raw)<13:
			intervals.append(raw)
			break
		for x in range(len(raw)):
			if raw[x]==",":
				intervals.append([raw[0:x-1],raw[x+1:-1]])
				break
	print(intervals)
	return intervals

def createSubclips(vPath, fType):
	fulls=glob.glob(vPath+"full/*")
	for x in range(len(fulls)):
		saveSubclips(vPath,fulls[x]+"/",fType)
	#print(fulls)

def offsetAudio(vPath, aPath, offsets, fType):
	temp=glob.glob(aPath+"silence/*")
	temp.sort()
	silence=[]
	for x in range(len(temp)):
		silence.append(AudioFileClip(temp[x]))
	#print(silence)
	subs=glob.glob(vPath+"subclips/*")
	subs.sort()
	#print(subs)
	buildOffsetClips(subs[0], silence, offsets, fType)


def buildOffsetClips(vPath, silence, offsets, fType):
	for x in range(len(vPath),0,-1):
		if vPath[x-1]=="/":
			vFile=vPath[x:]
			break
	aOffset=[]
	for x in range(len(offsets)):
		vBase=VideoFileClip(vPath+"/"+vFile+fType)
		aBase=vBase.audio
		vTemp=vBase
		temp=aBase.subclip("00:00:00."+offsets[x],aBase.duration)
		aTemp=concatenate_audioclips([temp,silence[x]])
		vTemp.audio=aTemp
		vTemp.write_videofile(vPath+"/"+vFile+"-"+offsets[x]+fType)
		vBase=VideoFileClip(vPath+"/"+vFile+fType)
		aBase=vBase.audio
		vTemp=vBase
		clipper=audioClipMask(offsets[x],aBase.duration)
		temp=aBase.subclip("00:00:00.000",clipper)
		aTemp=concatenate_audioclips([silence[x],temp])
		vTemp.audio=aTemp
		vTemp.write_videofile(vPath+"/"+vFile+"+"+offsets[x]+fType)
	print("Done for "+vFile)

	
	#For when the Audio comes before Video
	#aBase.subclip("00:00:00."+offsets[x],aBase.duration)

#Helper funtion to perform arithmatic on time strings in the format "HH:MM:SS.mm"
def audioClipMask(offset, duration):
	iOffset=int(offset)
	iDur=int(duration*1000)
	nDur=iDur-iOffset
	msDur=str(nDur%1000)
	nDur=int(nDur/1000)
	sDur=str(nDur%60)
	nDur=int(nDur/60)
	mDur=str(nDur%60)
	nDur=int(nDur/60)
	hDur=str(nDur)
	if len(sDur)==1:
		sDur="0"+sDur
	if len(mDur)==1:
		mDur="0"+mDur
	if len(hDur)==1:
		hDur="0"+hDur
	nDur=hDur+":"+mDur+":"+sDur+"."+msDur
	return nDur