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

    def __init__(self, fname,lname,email,role,userName):
        self.userName = userName
        self.fname = fname
        self.lname = lname
        self.email = email
        self.role = role