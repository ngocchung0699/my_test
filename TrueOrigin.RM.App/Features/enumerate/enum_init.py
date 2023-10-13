from cmd import IDENTCHARS
from enum import Enum, unique, Flag

class sBar(Enum) :
    IDLE            = 0
    INIT            = 1
    ACTION          = 2
    UPDATE          = 3
    EXPORT          = 4
    COUNT_TIME      = 5
    ERROR_NFC       = 6 
    ERROR_LOGOUT    = 7 
    CHANGE_RO       = 8 
    PAUSE           = 9
    READY           = 10
    ERROR_SERVER    = 11
    COMPLETE        = 12
    
class sMachine(Enum) :
    IDLE            = 0

    LOGIN           = 1000
    LOGIN_SUCCESS   = 1001
    LOGIN_FAILED    = 1002

    APPROVING       = 2
    WAIT_SERVER     = 3
    UPDATE_RO       = 4
    SELECT_RO       = 5
    CHANGE_RO       = 6
    READY           = 7
    RELEASING       = 8
    PAUSE           = 9
    STOP            = 10
    COMPLETE        = 11

class sReleasing(Enum) :
    IDLE            = 0
    INIT            = 1
    DETECT_STAMP    = 2
    PAUSE_PUSH      = 3
    TRY_COUNT       = 4
    ALARM_STOPSS    = 5
    CHECK           = 6
    UPDATE          = 7
    STOP            = 8
    NEXT_STAMP      = 9
    COMPLETE        = 10

class sRO(Enum) :
    APPROVING   = 0
    DISABLE     = 1
    READY       = 2
    RELEASING   = 3
    COMPLETE    = 4
    STOP        = 5
    PAUSE       = 6

class iRO(Enum) :
    id              = 0
    id_user         = 1
    id_batch        = 2
    id_producer     = 3
    id_product      = 4
    total_seri      = 5
    start_seri      = 6
    current_seri    = 7
    stat_result     = 8
    timegm          = 9

class sMC(Enum) :
    READY       = 0
    RELEASING   = 1
    CHANG_RO    = 2
    CHANGE_MC   = 3

class iUser(Enum):
    ID          = 0
    NAME        = 1
    EMAIL       = 2
    SEX         = 3
    PICTURE     = 4

