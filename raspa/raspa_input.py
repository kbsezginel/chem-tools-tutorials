"""
Generates RASPA input file for given cif file and simulation parameters to calculate adsorption.
"""
# RASPA 2 input file generation for adsorption simulations
# Author: Kutay B. Sezginel
# Date: July 2017


def write_raspa_file(input_file, config):
    """
    Writes RASPA input file for simulating gas adsorption.
    Arguments:
        - input_file (str)     : path to input file.
        - config (dict)        : RASPA simulation config dictionary
    """
    external_pressure = float(config['pressure']) * 100000  # bar -> torr

    with open(input_file, "w") as raspa_input_file:
        raspa_input_file.write(
            "SimulationType                 MonteCarlo\n" +
            "NumberOfCycles                 %s\n" % config['cycles'] +
            "NumberOfInitializationCycles   %s\n" % config['init_cycles'] +
            "PrintEvery                     %i\n" % config['print_every'] +
            "RestartFile                    no\n" +
            "\n" +
            "Forcefield                     %s\n" % config['forcefield'] +
            "CutOff                         %.2f\n" % config['cutoff'] +
            "\n" +
            "Framework                      0\n" +
            "FrameworkName                  %s\n" % config['framework'] +
            "UnitCells                      %i %i %i\n" % tuple(config['unitcell']) +
            "ExternalTemperature            %.1f\n" % config['temperature'] +
            "ExternalPressure               %.1f\n" % external_pressure +
            "\n"
        )
        if config['charge'] == 'yes':
            raspa_input_file.write(
                "Charge Method                  Ewald\n" +
                "Ewald Precision                1e-6\n" +
                "UseChargesFromCIFFile          yes\n"
            )

        if config['void_fraction'] is not False:
            raspa_input_file.write("HeliumVoidFraction             %s\n" % str(vf))
        if config['movies'] == 'yes':
            raspa_input_file.write(
                "\n" +
                "Movies                         yes\n" +
                "WriteMoviesEvery               %i\n" % movies
            )
        for comp_idx, component in enumerate(config['components']):
            # TODO: Handle mixture adsorption!!!!!!!!!!!!!!!!!!
            raspa_input_file.write(
                "\n" +
                "Component %-4iMoleculeName               %s\n" % (comp_idx, component['name']) +
                "              MoleculeDefinition         %s\n" % component['definition'] +
                "              TranslationProbability     %.2f\n" % component['p_translation'] +
                "              RotationProbability        %.2f\n" % component['p_rotation'] +
                "              ReinsertionProbability     %.2f\n" % component['p_reinsertion'] +
                "              SwapProbability            %.2f\n" % component['p_swap'] +
                "              CreateNumberOfMolecules    %i\n" % component['create_molecules']
            )
