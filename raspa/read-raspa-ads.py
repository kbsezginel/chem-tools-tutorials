"""
Read RASPA output file for gas adsorption simulations.
"""
import os
import sys
import glob


def parse_output(data_file, adsorbate='ADSORBATE', verbose=False):
    """Parse output file for gas adsorption data.
    Args:
        data_file (str): path to RASPA simulation output file.
    Returns:
        results (dict): absolute and excess molar, gravimetric, and volumetric
            gas loadings, as well as energy of average, van der Waals, and
            Coulombic host-host, host-adsorbate, and adsorbate-adsorbate
            interactions.
    """
    results = dict(ads=dict(absolute=dict(), excess=dict()), energy=dict(), warnings=[], finished=False, initialization=False)
    with open(data_file) as ads_data:
        data_lines = ads_data.readlines()

    for i, line in enumerate(data_lines):
        if 'Simulation finished' in line:
            results['finished'] = True
            results['initialization'] = True
        if 'Average loading absolute [molecules/unit cell]' in line:
            results['ads']['absolute']['mol/uc'] = float(data_lines[i].split()[5])
            results['ads']['absolute']['mol/kg'] = float(data_lines[i + 1].split()[5])
            results['ads']['absolute']['mg/g'] = float(data_lines[i + 2].split()[5])
            results['ads']['absolute']['cc/g'] = float(data_lines[i + 3].split()[6])
            results['ads']['absolute']['cc/cc'] = float(data_lines[i + 4].split()[6])
        elif 'Average loading excess [molecules/unit cell]' in line:
            results['ads']['excess']['mol/uc'] = float(data_lines[i].split()[5])
            results['ads']['excess']['mol/kg'] = float(data_lines[i + 1].split()[5])
            results['ads']['excess']['mg/g'] = float(data_lines[i + 2].split()[5])
            results['ads']['excess']['cc/g'] = float(data_lines[i + 3].split()[6])
            results['ads']['excess']['cc/cc'] = float(data_lines[i + 4].split()[6])
        elif 'Average Host-Host energy' in line:
            results['energy']['host_host_avg'] = float(data_lines[i + 8].split()[1])
            results['energy']['host_host_vdw'] = float(data_lines[i + 8].split()[5])
            results['energy']['host_host_cou'] = float(data_lines[i + 8].split()[7])
        elif 'Average Adsorbate-Adsorbate energy' in line:
            results['energy']['ads_ads_avg'] = float(data_lines[i + 8].split()[1])
            results['energy']['ads_ads_vdw'] = float(data_lines[i + 8].split()[5])
            results['energy']['ads_ads_cou'] = float(data_lines[i + 8].split()[7])
        elif 'Average Host-Adsorbate energy' in line:
            results['energy']['host_ads_avg'] = float(data_lines[i + 8].split()[1])
            results['energy']['host_ads_vdw'] = float(data_lines[i + 8].split()[5])
            results['energy']['host_ads_cou'] = float(data_lines[i + 8].split()[7])
        elif 'WARNING' in line:
            results['warnings'].append(line)

#   If simulation is not finished ------------------------------------------------------------------
    if not(results['finished']):
        for i, line in enumerate(data_lines):
            if 'Current cycle' in line and line[0] == 'C':  # If production cycle
                results['cycle'] = int(line.split()[2])
                results['initialization'] = True
            if 'Loadings per component' in line and results['initialization']:
                results['ads']['absolute']['mol/uc'] = float(data_lines[i + 3].split()[2])
                results['ads']['absolute']['mol/kg'] = float(data_lines[i + 3].split()[6])
                results['ads']['absolute']['mg/g'] = float(data_lines[i + 3].split()[10])
                results['ads']['absolute']['cc/g'] = float(data_lines[i + 4].split()[0])
                results['ads']['absolute']['cc/cc'] = float(data_lines[i + 4].split()[5])

                results['ads']['excess']['mol/uc'] = float(data_lines[i + 5].split()[2])
                results['ads']['excess']['mol/kg'] = float(data_lines[i + 5].split()[6])
                results['ads']['excess']['mg/g'] = float(data_lines[i + 5].split()[10])
                results['ads']['excess']['cc/g'] = float(data_lines[i + 6].split()[0])
                results['ads']['excess']['cc/cc'] = float(data_lines[i + 6].split()[5])

    if verbose:
        print(
            "\n%-15s\tabsolute\texcess\n" % adsorbate +
            "mol/uc\t\t%8.3f\t%8.3f\n" % (results['ads']['absolute']['mol/uc'], results['ads']['excess']['mol/uc']) +
            "mg/g\t\t%8.3f\t%8.3f\n" % (results['ads']['absolute']['mg/g'], results['ads']['excess']['mg/g']) +
            "cc/cc\t\t%8.3f\t%8.3f\n" % (results['ads']['absolute']['cc/cc'], results['ads']['excess']['cc/cc'])
        )
        if len(results['warnings']) > 0:
            print('%s - %i warning(s) found -> %s' % (data_file, len(warnings), warnings[0].strip()))

    return results


if __name__ == "__main__":
    ads_path = glob.glob(os.path.join(sys.argv[-1], 'Output', 'System_0', '*.data'))[0]
    adsorbate = os.path.split(sys.argv[-1])[-1]
    parse_output(ads_path, adsorbate=adsorbate, verbose=True)
