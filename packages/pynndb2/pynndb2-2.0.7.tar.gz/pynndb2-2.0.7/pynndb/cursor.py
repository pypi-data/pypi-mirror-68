#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from lmdb import Cursor as LMDBCursor


class Cursor:
    """
    The Cursor class is a simple wrapper for the LMDB cursor object, it's
    primary goal is to ensure that functions returning with "keyonly" set employ
    proper Python strings rather than 'bytes' arrays.
    """

    def __init__(self, cursor: LMDBCursor) -> None:
        """
        Simply set the "key" and "val" attributes of the object to the values
        we want to make available to the library user.

        cursor - an LMDB cursor object which has a reference to both the data key and value
        """
        self.key = cursor.key()
        self.val = cursor.value().decode()
