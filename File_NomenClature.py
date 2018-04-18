import os
from pyexcel_xls import get_data
import json
from shutil import copyfile

CommanPath = '/home/kwantics/GitPractice/File_Format/'
#CommanPath is string which is change according to system path.

def ReadXlsFile():
    #ReadXlsFile is function that read data from SpeakerMapping.xlsx .
    #Return data of List, which stored speaker data(ID,Name,Gender).
    temppath=CommanPath+'AllFiles/SpeakerMapping.xlsx'
    data = get_data(temppath)
    jsontempdata=json.loads(json.dumps(data))
    data= jsontempdata['Sheet1']
    data.pop(0)
    return data

def Main():
    """
    Main() create a dictionary which stored Name,Gender,SpeakerID,Path,TextFile(List),VoiceFile(List).
    Return  FileInfo dictionary
    """
    SpeakerInfo=ReadXlsFile()
    AllFolderList=os.listdir(CommanPath)
    AllFolderList.remove('AllFiles')
    FileInfo={}
    for item in AllFolderList:
        UserInfo={}
        UserInfo['Name']=item
        path=CommanPath + item + '/'
        VaktaList= os.listdir(path)
        Vakta=VaktaList[0]
        UserInfo['Path']=path+Vakta
        TempPath=path+Vakta+'/callText'
        CallText= os.listdir(TempPath)
        UserInfo['CallText']=CallText
        TempPath=path+Vakta+'/callVoice'
        CallVoice= os.listdir(TempPath)
        UserInfo['CallVoice']=CallVoice

        new_list = [[y for y in x if x[1] == item] for x in SpeakerInfo]
        SpeakerList = [x for x in new_list if x]

        Gender=str(SpeakerList[0][3])
        Speaker_ID=SpeakerList[0][2]
        Vakta_Version=SpeakerList[0][4]
        Age_Range=SpeakerList[0][5]

        UserInfo['Gender'] = Gender
        UserInfo['SpeakerID']=Speaker_ID
        UserInfo['Vakta_Version'] = Vakta_Version
        UserInfo['Age_Range']=Age_Range

        FileInfo[item] = UserInfo

    return FileInfo

def File_NomenClature(FileData):
    """
    File_NomenClature function which collect all text and Voice file and rename file example H1_S2_M_2.txt and
     H1_S2_M_2.3gpp
    Both rename  file save in AllFiles folders.
    :param FileData Type dictionary,dictionary=Name,Gender,SpeakerID,Path,TextFile(List),VoiceFile(List)
    """
    global number
    number=1

    # Following TextLocation and VoiceLocation is location where after rename all file will be stored.
    TextLocation=CommanPath+'AllFiles/callTextAll/'
    VoiceLocation=CommanPath+'AllFiles/callVoiceAll/'

    for item in FileData:
        Metadata=FileData[item]
        ID=Metadata['SpeakerID']
        Gender=Metadata['Gender']
        Path=Metadata['Path']
        Age_Range=Metadata['Age_Range']
        Vakta_Version=Metadata['Vakta_Version']
        CallVoiceList=Metadata['CallVoice']
        CallTextList = Metadata['CallText']

        #Extract Voice File Name in List
        VoiceExist=[x.split('.')[0] for x in CallVoiceList]
        # Extract Text File Name in List
        TextExist = [x.split('.')[0] for x in CallTextList]
        TextExist=list(map(int, TextExist))
        TextExist.sort()

        # File rename and file transfer action perform here.
        for i in TextExist:
            if str(i) in VoiceExist:
                TextSrc=Path+'/callText/'+str(i)+'.txt'
                VoiceSrc = Path + '/callVoice/' + str(i) + '.3gpp'
                TextFileName='H'+str(number)+'_S'+str(ID)+'_'+ Gender+str(Age_Range) + '_V'+str(Vakta_Version)+'_' + str(i)+'.txt'
                VoiceFileName = 'H' + str(number) + '_S' + str(ID) + '_' + Gender+str(Age_Range) + '_V'+str(Vakta_Version)+'_'+ str(i) + '.3gpp'
                TextDestination=TextLocation+TextFileName
                VoiceDestination = VoiceLocation + VoiceFileName
                copyfile(TextSrc, TextDestination)
                copyfile(VoiceSrc, VoiceDestination)
                number+=1

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
        command = " ffmpeg -i " + fileAddress_3gpp + "/" + item + " -ac 1 -acodec pcm_s16le -ar 8000 /home/kwantics/GitPractice/File_Format/AllFiles/callVoiceAllWavFile/"+waveFileName
        #Execution of command start here.
        os.system(command)

if __name__ == "__main__":
    #Program Start from here.Main Function is calling which return a dictionary.
    FileData=Main()
    """
    FileData is collection of all data in dictionary form
    Name,Gender,SpeakerID,Path,TextFile(List),VoiceFile(List)
    """
    File_NomenClature(FileData)
    #function wav_from_3gpp calling that convert all 3gpp file into wav file.
    wav_from_3gpp()
    print('File nomenclature and rename all file transfer move successfully completed.')
