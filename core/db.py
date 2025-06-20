##############
#
#     @
#       @
#   @ @ @
#
##############


VALID_USERS = {}


def get_valid_users():
    return VALID_USERS


def set_valid_users(valid_users: dict):
    global VALID_USERS
    VALID_USERS = valid_users
