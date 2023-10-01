from telethon.sync import Button

def Inline(DataList , DoneMessage = None , Data = None) :
    # i want to inline buttons seprate two by two for this : 
    
    Buttons = list(map(lambda DataIndex : [Button.inline(DataList[DataIndex] , data =Data) ,\
            Button.inline(DataList[DataIndex + 1] , data = Data)] \
            if DataIndex + 1 != len(DataList) else [Button.inline(DataList[DataIndex] , data = Data)] ,\
            range(len(DataList))[::2] ))
   
    # this is for i want the done button be big and seprated
    if DoneMessage : 
        Buttons.append([Button.inline(DoneMessage)]) 

    return Buttons

def Url(Names , Links , DoneMessage = None) :
    Buttons = list(map(lambda Index : [Button.url(Names[Index] , Links[Index]) , Button.url(Names[Index + 1] , Links[Index + 1])] \
            if Index + 1 != len(Links) else [Button.url(Names[Index] , Links[Index])] ,\
            range(len(Links))[::2] ))

    # this is for i want the done button be big and seprated
    if DoneMessage : 
        Buttons.append([Button.inline(DoneMessage)]) 

    return Buttons
