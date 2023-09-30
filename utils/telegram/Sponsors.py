
def Data() : 
    with open('../database/SponsorsData.json' , 'r') as File : 
        Datas = json.load(File)

    return Datas

def Remove(Name) :  
    Datas = Data()
    Datas = {'Channels' : list(filter(lambda Channels : Channels['Name'] != Name , Datas['Channels']))}

    with open('../database/SponsorsData.json' , 'w' ) as File : 
        json.dump(Datas , File , indent = 4)
    
    return list(map(lambda Channels : Channels['Name'] , Datas['Channels']))

def Add(ChannelName , ChannelLink) : 
    Data = Data()
    
    Data['Channels'].append({'Name' : ChannelName , 'Link' : ChannelLink , 'Date' : datetime.now().isoformat()})
    
    with open('../database/SponsorsData.json' , 'w') as File : 
        json.dump(Data  , File , indent = 4)
