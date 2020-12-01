from paste_printer.command.command import Command
from paste_printer.command.tasks import Writer_Task, Parser_Task
from paste_printer.gcode_manipulation.gcode_parser import GCode_Parser
from paste_printer.gcode_manipulation.gcode_writer import Gcode_Writer
from paste_printer.util.file_handler import File_Handler

class Command_Executor:

    def __init__(self, command: Command):
        self.command = command
        self.file_handler = File_Handler()

        self.gcode = None
        self.gcode_parser = None
        self.gcode_writer = Gcode_Writer()

    def execute(self):
        #Read the gcode from file
        line_list = self.file_handler.read_gcode_file(file_path=self.command.path_to_file)

        #Setup GCode Parser
        self.gcode_parser = GCode_Parser(line_list=line_list)

        #Create new gcode
        self.execute_parser_task(Parser_Task.CREATE_GCODE)

        #Set Flowrate other layers
        self.execute_writer_task(Writer_Task.SET_FLOWRATE_LAYER_0, self.command.flow_rate_layer_0)

        #Set Flowrate other layers
        self.execute_writer_task(Writer_Task.SET_FLOWRATE_OTHER_LAYERS, self.command.flow_rate_other_layers)

        #Set bed temperature
        self.execute_writer_task(Writer_Task.SET_BED_TEMPERATURE, self.command.bed_temperature)

        #Check if add information was ticked
        if self.command.additional_information_bol == True:
            self.execute_writer_task(Writer_Task.ADDITIONAL_INFORMATION)

        #Check if pause after each layer was ticked
        if self.command.pause_each_layer_bol == True:
            self.execute_writer_task(Writer_Task.PAUSE_EACH_LAYER, self.command.pause_each_layer_par)

        # Check if retract syringe was ticked
        if self.command.retract_syringe_bol == True:
            self.execute_writer_task(Writer_Task.RETRACT_SYRINGE)

        # Improve the gcode at the end (i.e. add start timer)
        self.execute_parser_task(Parser_Task.IMPROVE_GCODE_AT_END)

        # Create final gcode(combine all parts into one)
        self.execute_parser_task(Parser_Task.CREATE_FINAL_GCODE)

        #Write to file
        self.file_handler.write_file(gcode=self.gcode, path=self.command.storage_path, file_name=self.command.file_name)

    def execute_writer_task(self, writer_task, parameter_1 = None):

        self.gcode_writer.set_gcode(self.gcode)

        if writer_task == Writer_Task.SET_FLOWRATE_LAYER_0:
            result_gcode = self.gcode_writer.set_flowrate_layer_0(parameter_1)
        if writer_task == Writer_Task.SET_FLOWRATE_OTHER_LAYERS:
            result_gcode = self.gcode_writer.set_flowrate_other_layers(parameter_1)
        if writer_task == Writer_Task.SET_BED_TEMPERATURE:
            result_gcode = self.gcode_writer.set_bed_temperature(parameter_1)

        if writer_task == Writer_Task.ADDITIONAL_INFORMATION:
            result_gcode = self.gcode_writer.additional_information()
        if writer_task == Writer_Task.PAUSE_EACH_LAYER:
            result_gcode = self.gcode_writer.pause_each_layer(parameter_1)
        if writer_task == Writer_Task.RETRACT_SYRINGE:
            result_gcode = self.gcode_writer.retract_syringe()

        self.gcode = result_gcode
        self.execute_parser_task(Parser_Task.FIND_INDEXES)

    def execute_parser_task(self, parser_task):

        self.gcode_parser.set_gcode(self.gcode)

        if parser_task == Parser_Task.CREATE_GCODE:
            result_gcode = self.gcode_parser.create_gcode()
        if parser_task == Parser_Task.FIND_INDEXES:
            result_gcode = self.gcode_parser.find_indexes()
        if parser_task == Parser_Task.IMPROVE_GCODE_AT_END:
            result_gcode = self.gcode_parser.improve_gcode_at_the_end()
        if parser_task == Parser_Task.CREATE_FINAL_GCODE:
            result_gcode = self.gcode_parser.create_final_gcode()

        self.gcode = result_gcode