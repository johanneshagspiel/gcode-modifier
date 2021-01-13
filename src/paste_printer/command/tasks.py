from enum import Enum

class Writer_Task (Enum):
    SET_FLOWRATE_LAYER_0 = 1
    SET_FLOWRATE_OTHER_LAYERS = 2
    SET_FLOWRATE_OUTER_INFILL = 3
    SET_BED_TEMPERATURE = 4
    SET_PRINT_SPEED = 5
    TURN_ON_FAN = 6

    ADDITIONAL_INFORMATION = 7
    PAUSE_EACH_LAYER = 8
    CLEAN_NOZZLE = 9
    RETRACT_SYRINGE_AT_END = 10
    BIG_SYRINGE = 11

class Parser_Task (Enum):
    CREATE_GCODE = 1
    FIND_INDEXES = 2

    IMPROVE_GCODE_AT_END = 3
    CREATE_FINAL_GCODE = 4