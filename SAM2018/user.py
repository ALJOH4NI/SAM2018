from aetypes import Enum
class Role(Enum):
    PCC = 'PCC'
    Author = 'Author'
    PCM = 'PCM'
    Admin = 'Admin'


class user:
    fname = ""
    lname = ""
    email = ""
    role =  Role.Author
    userName = ""
    password = "123"
    def __init__(self, fname,lname,email,role,userName,password):
        self.userName = userName
        self.fname = fname
        self.lname = lname
        self.email = email
        self.role = role
        self.password = password