def JsonFile(Path) :
    try : 
        with open(Path , 'r') as File : 
            json.load(File)

        return True

    except : 
        return False
