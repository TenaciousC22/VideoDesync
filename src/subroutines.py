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

#convert .mov files to mp4 files using the x264 codec
def convertToMP4(vPath):
	fulls=glob.glob(vPath+"full/*")
	fulls.sort()
	for x in range(len(fulls)):
		path=fulls[x]
		folder=glob.glob(path+"/*")
		for y in range(len(folder)):
			file=folder[y]
			print(file)
			if file[-3:]=="MOV":
				video=VideoFileClip(file)
				video.write_videofile(vPath+"full/speaker"+str(x+1)+"/speaker"+str(x+1)+".mp4",codec="libx264")

def addFixedAudio(vPath):
	fulls=glob.glob(vPath+"full/*")
	fulls.sort()
	for x in range(len(fulls)):
		temp=glob.glob(fulls[x]+"/*")
		if len(temp)==3:
			video=VideoFileClip(fulls[x]+"/speaker"+str(x+1)+".mp4")
			audio=AudioFileClip(fulls[x]+"/modified.wav")
			#print(audio.duration)
			final=video.set_audio(audio)
			final.write_videofile(fulls[x]+"/speaker"+str(x+1)+".mp4")

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

def saveSubclips(vPath, path, fType, number):
	cPath=os.getcwd()
	intervals=extractIntervals(path)
	vFile=glob.glob(path+"*"+fType)
	vFile.sort()
	vFile=vFile[0]
	if not os.path.isdir(cPath+"/"+vPath+"subclips/speaker"+str(number+1)):
		os.mkdir(cPath+"/"+vPath+"subclips/speaker"+str(number+1))
		for x in range(len(intervals)):
			os.mkdir(cPath+"/"+vPath+"subclips/speaker"+str(number+1)+"/clip"+str(x+1))
	for x in range(len(vFile),0,-1):
		if vFile[x-1]=="/":
			vFile=vFile[x:-4]
			break
	for x in range(len(intervals)):
		clip=VideoFileClip(path+vFile+fType)
		sub=clip.subclip(intervals[x][0],intervals[x][1])
		sub.write_videofile(vPath+"subclips/speaker"+str(number+1)+"/clip"+str(x+1)+"/base"+fType)

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
	fulls.sort()
	cwd=os.getcwd()
	if not os.path.isdir(cwd+"/"+vPath+"subclips"):
		os.mkdir(cwd+"/"+vPath+"subclips/")
	for x in range(len(fulls)):
		saveSubclips(vPath,fulls[x]+"/",fType, x)
	#print(fulls)

def offsetAudio(vPath, aPath, offsets, fType):
	temp=glob.glob(aPath+"silence/*")
	temp.sort()
	silence=[]
	for x in range(len(temp)):
		silence.append(AudioFileClip(temp[x]))
	#print(silence)
	speakers=glob.glob(vPath+"subclips/*")
	speakers.sort()
	#print(subs)
	for i in range(len(speakers)):
		clips=glob.glob(speakers[i]+"/*")
		clips.sort()
		clips.sort(key=len)
		#print(clips)
		for x in range(len(clips)):
			buildOffsetClips(clips[x], silence, offsets, fType)


def buildOffsetClips(vPath, silence, offsets, fType):
	vFile="base"
	aOffset=[]
	for x in range(len(offsets)):
		vBase=VideoFileClip(vPath+"/"+vFile+fType)
		aBase=vBase.audio
		vTemp=vBase
		temp=aBase.subclip("00:00:00."+offsets[x],aBase.duration)
		aTemp=concatenate_audioclips([temp,silence[x]])
		vTemp.audio=aTemp
		vTemp.write_videofile(vPath+"/"+"I"+offsets[x]+fType)
		vBase=VideoFileClip(vPath+"/"+vFile+fType)
		aBase=vBase.audio
		vTemp=vBase
		clipper=audioClipMask(offsets[x],aBase.duration)
		temp=aBase.subclip("00:00:00.000",clipper)
		aTemp=concatenate_audioclips([silence[x],temp])
		vTemp.audio=aTemp
		vTemp.write_videofile(vPath+"/"+"B"+offsets[x]+fType)
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

def jumble(vPath):
	temp=glob.glob(vPath+"subclips/*")
	for x in range(len(temp)):
		#This is mostly to ensure that every file has a compatible one to jumble with
		#viewlen(vPath,x+1)
		#jumble the audio
		jumbler(vPath,x+1)
		print("")
	#for x in range(len(temp)):

def jumbler(vPath,number):
	cliplist=glob.glob(vPath+"subclips/speaker"+str(number)+"/*")
	cliplist.sort()
	cliplist.sort(key=len)
	clips=[]
	index=[]
	audio=[]
	for x in range(len(cliplist)):
		clips.append(VideoFileClip(cliplist[x]+"/base.mp4"))
	for x in range(len(clips)):
		index.append(x+1)
	for x in range(len(clips)):
		for y in range(x+1,len(clips)):
			if(clips[y].duration<clips[x].duration):
				temp=clips[y]
				clips[y]=clips[x]
				clips[x]=temp
				temp=index[y]
				index[y]=index[x]
				index[x]=temp
	for x in range(len(clips)):
		audio.append(clips[x].audio)
	x=0
	for y in range(len(clips)):
		if(clips[y].duration>clips[x].duration):
			clips[y-1].audio=audio[x]
			clips[y-1].write_videofile(vPath+"subclips/speaker"+str(number)+"/clip"+str(index[x])+"/jumble.mp4")
			for z in range(x+1,y):
				clips[z-1].audio=audio[z]
				clips[z-1].write_videofile(vPath+"subclips/speaker"+str(number)+"/clip"+str(index[z])+"/jumble.mp4")
			x=y
	clips[len(clips)-1].audio=audio[x]
	clips[len(clips)-1].write_videofile(vPath+"subclips/speaker"+str(number)+"/clip"+str(index[x])+"/jumble.mp4")
	for z in range(x+1,len(clips)):
		clips[z-1].audio=audio[z]
		clips[z-1].write_videofile(vPath+"subclips/speaker"+str(number)+"/clip"+str(index[z])+"/jumble.mp4")

def viewlen(vPath,number):
	clips=[]
	lengths=[]
	cliplist=glob.glob(vPath+"subclips/speaker"+str(number)+"/*")
	cliplist.sort()
	cliplist.sort(key=len)
	for x in range(len(cliplist)):
		clips.append(VideoFileClip(cliplist[x]+"/base.mp4"))
	for x in range(len(clips)):
		lengths.append(clips[x].duration)
	lengths.sort()
	for x in range(len(lengths)):
		print(lengths[x])