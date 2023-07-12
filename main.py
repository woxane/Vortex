import os



def ConfigCheck() : 
    if not os.path.exists('config.py') : 
        InstaUsername = input('Enter your Instagram Username : ')
        InstaPass = input('Enter your Instagram Password : ')

        with open('config.py' , 'w') as File : 
            File.write(f'InstaUsername = "{InstaUsername}"')
            File.write(f'\nInstaPass = "{InstaPass}"')




if __name__ == '__main__' : 
    ConfigCheck()
