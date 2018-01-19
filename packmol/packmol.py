"""
Generate packmol input file and run packmol.
"""
import os
import shutil
import subprocess


class Packmol:
    """
    Wrapper class for the packmol molecule packer program
    """
    def __init__(self, options={}, structures=[]):
        """
        packmol

        Args:
        - options (dict): Options to be used in input file
        - structure (list): List of structures (dict)
        """
        self.clear()
        self.structures = structures
        # Default options
        self.options = {'command_line': 'packmol',
                        'seed': None,
                        'tolerance': 3.0,
                        'filetype': 'xyz',
                        'output': 'packed.xyz',
                        'input': 'packmol.inp'
                        }
        self.set_options(options)

    def clear(self):
        self.structures = []
        self.options = {}

    def set_options(self, options):
        """Update packmol option values.

        Use keyword list to change the value of packmol options."""
        for key, value in options.items():
            self.options[key] = value

    def add_structure(self, structure):
        """Add one or more structure group to be packed by packmol.

        Args:
            - structure (dict): Structure information -> {'structure': file_name, 'number': count, 'position': {'fixed': '40. 40. 40. 0. 0. 0.'}}
        """
        self.structures.append(structure)

    def _get_input_file(self):
        """
        Create input file for Packmol run.
        """
        self.input_file = os.path.join(self.run_dir, self.options['input'])
        with open(self.input_file, 'w') as inp:
            inp.write('tolerance      %.2f\n' % self.options['tolerance'])
            inp.write('filetype       %s\n' % self.options['filetype'])
            inp.write('output         %s\n' % self.options['output'])
            inp.write('\n########################################################################\n')
            for s in self.structures:
                inp.write('structure      %s\n' % s['structure'])
                inp.write('number         %s\n' % str(s['number']))
                for key, value in s['position'].items():
                    inp.write('  %-15s %15s\n' % (key, value))
                inp.write('end structure\n\n')

    def _set_run(self, run_dir, source_dir):
        """
        Setup packmol run.
        """
        self.run_dir = run_dir
        os.makedirs(run_dir, exist_ok=True)
        shutil.copy(os.path.join(source_dir, self.options['command_line']), os.path.join(run_dir, self.options['command_line']))
        for s in self.structures:
            shutil.copy(os.path.join(source_dir, s['structure']), os.path.join(run_dir, s['structure']))

    def run(self, run_dir, source_dir):
        """
        Run packmol.
        """
        self._set_run(run_dir, source_dir)
        self._get_input_file()
        input_file = open(self.input_file, 'r')
        self.output_file = open(os.path.join(self.run_dir, 'packmol.out'), 'w')
        subprocess.call('./%s' % self.options['command_line'], stdin=input_file, stdout=self.output_file, cwd=run_dir)
        self.output_file.close()
        input_file.close()

####################################################################################################

    # def _prepare_input_file (self) :
    #     """Create temp file to be used as packmol input file
    #
    #     This method is for internal use only.  Content of the file can be accessed from
    #     instance variable ``_input_stash`` after the method.
    #
    #     Returns:
    #         A named temporary file that contains options as well as structure definitions
    #         formated as packmol input."""
    #     inp_file = tempfile.NamedTemporaryFile(mode="w+",suffix="inp")
    #     inp_file.write("filetype xyz\n")
    #
    #     ranseed=self._options["seed"]
    #     if not ranseed : ranseed=time.clock()
    #     inp_file.write("seed {}\n".format(hash(ranseed)%10**9))
    #
    #     # Write down other arguments
    #     for key,value in self._options.items():
    #         if key not in Packmol.NONPACKMOL_OPTIONS:
    #             inp_file.write("{0} {1}\n".format(key,value))
    #     #
    #     for mol_type in self._structure_list :
    #         inp_file.write("structure {}\n".format(mol_type["structure"].name))
    #         inp_file.write("  number {}\n".format(mol_type["number"]))
    #         if self._options["region_type"] == "sphere" :
    #             inp_file.write(
    #                 "  inside sphere 0.0 0.0 0.0 {}\n".format(self._options["dimension"]))
    #         elif self._options["region_type"] :
    #             raise NotImplementedError("Currently only sphere regions are supported.")
    #         for key,value in mol_type["options"].items():
    #             inp_file.write("  {0} {1}\n".format(key,value))
    #         inp_file.write("end structure\n")
    #     inp_file.flush()
    #     inp_file.seek(0)
    #     self._input_stash=inp_file.read()
    #     inp_file.seek(0)
    #     return inp_file
    #
    #
    # def clear(self):
    #     """Clean the molecule table."""
    #     self._structure_list=[]
    #
    #
    #
    #
    #
    #
    # def pack(self, output=None) :
    #     """Perform packmol runs.
    #
    #     Construct input file then creates a subprocess to run packmol.
    #
    #     Args:
    #         output: Specify the filename of the packed molecule geometry file.
    #
    #     Return is a dict that contains the following fields:
    #         "filename" :  Filename of the packed geoemtry file.
    #         "packmol output" : Print out from packmol run.
    #     """
    #     if output :
    #         self._options["output"] = output
    #     outfile = tempfile.NamedTemporaryFile(mode="w+")
    #     code = subprocess.call(self._options["command_line"], stdin=self._prepare_input_file(),
    #                     stdout=outfile )
    #     outfile.seek(0)
    #     self._output_stash = outfile.read()
    #     if code :
    #         raise Exception("Packmol error termination. exit code={}".format(code))
    #     if "ERROR" in self._output_stash :
    #         raise Exception("Individual molecules cannot be staged in packing region. " +
    #                         "Increase tolerance value.")
    #     if "STOP" in self._output_stash :
    #         raise FailToPack(("Packing failed.  Cannot fulfill tolerance constraints. " +
    #                        "Best result found in [{}]").format(self._options["output"]))
    #     self._last_result={"filename":self._options["output"],"packmol output":self._output_stash}
    #     if _has_openbabel :
    #         self._packed = pb.readfile("xyz",self._options["output"]).next()
    #         ff=pb._forcefields[self._options['opt_force_field']]
    #         ff.Setup(self._packed.OBMol)
    #         self._last_result["energy"]=ff.Energy()
    #     return self._last_result
