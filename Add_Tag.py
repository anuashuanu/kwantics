import os

TextFileLocation="/home/kwantics/GitPractice/callTextAll"
WaveFileLocation="/home/kwantics/GitPractice/File_Format/AllFiles/callVoiceAllWavFile"

def AddString():
    #This Function Add String Start and End of the file.
    # <s> HINDI TEXT </s> (wavFolder/wavFilename)

    AllFileList = os.listdir(TextFileLocation)
    #AllFileList is list of all text file.
    for File in AllFileList:
        fileNameWithPath=TextFileLocation+'/'+File
        FileNameWithoutExt=File.split('.')[0]
        StartString='<s> '
        EndString=" <s> " +'('+WaveFileLocation+'/'+FileNameWithoutExt  +')'
        f = open(fileNameWithPath, 'r+')
        lines = f.readlines()  # read old content
        f.seek(0)  # go back to the beginning of the file
        f.write(StartString)  # write new content at the beginning
        for line in lines:  # write old content after new
            f.write(line)
        with open(fileNameWithPath, 'a') as f:
            f.write(EndString)
        f.close()

if __name__ == "__main__":
    AddString()