# FTP部分协议
# 本部分参考FTP协议，进行了简化

class FTPProtolSever(object):
    def __init__(self):
        pass

    # register
    def register(self, date):
        user_id, password = None, None
        thread_level = 1
        date_base = "user_db"
        op = "insert"
        date = [user_id, password]

    # login
    def login(self, date):
        user_id, password = None, None
        thread_level = 1
        date_base = "user_db"
        op = "select"
        date = [user_id, password]

    # pwd
    def pwd(self):
        return None

    # ls_all
    def ls_all(self):
        user_id = None
        thread_level = 1
        date_base = "user_index_db"
        op = "select"
        date = user_id
        file_tree = None
        return file_tree

    # ls
    def ls(self):
        file_tree = None

    # cd
    def cd(self):
        file_tree = None

    # mkdir
    def mkdir(self):
        file_tree = None
        user_id = None
        thread_level = 1
        date_base = "user_index_db"
        op = "update"
        date = user_id
        file_tree = None
        return file_tree

    # put
    def put(self):
        file_tree = None
        user_id = None
        thread_level = 1
        date_base = "user_index_db"
        op = "update"
        date = user_id
        file_tree = None
        return file_tree

    # get
    def get(self):
        pass

    # delete
    def delete(self):
        file_tree = None
        user_id = None
        thread_level = 1
        date_base = "user_index_db"
        op = "update"
        date = user_id
        file_tree = None
        return file_tree

    # exit
    def exit(self):
        pass


class FTPProtolClient(object):
    def __init__(self):
        pass

    # register
    def register(self):
        pass

    # login
    def login(self):
        pass

    # pwd
    def pwd(self):
        pass

    # ls_all
    def ls_all(self):
        pass

    # ls
    def ls(self):
        pass

    # cd
    def cd(self):
        pass

    # mkdir
    def mkdir(self):
        pass

    # put
    def put(self):
        pass

    # get
    def get(self):
        pass

    # delete
    def delete(self):
        pass

    # exit
    def exit(self):
        pass