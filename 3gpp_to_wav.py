import os

def wav_from_3gpp():
    #wav_from_3gpp function convert 3gpp file into wav file.
    #3gpp file address here.
    fileAddress_3gpp='/home/kwantics/GitPractice/File_Format/AllFiles/callVoiceAll'
    #AllFileList is list that contains all 3gpp file name
    AllFileList=os.listdir(fileAddress_3gpp)

    for item in AllFileList:
        #extract file name and split from '.'
        fileName=item.split('.')[0]
        # create wav file Name.
        waveFileName=fileName+'.wav'
        #create command that convert 3gpp file into wav file.
        command="ffmpeg -i " +fileAddress_3gpp+ "/"+item + " -c:a libmp3lame /home/kwantics/GitPractice/File_Format/AllFiles/callVoiceAllWavFile/" + waveFileName
        print(command)
        #Execution of command start here.
        os.system(command)

wav_from_3gpp()