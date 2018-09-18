"""
Read RASPA output file for gas adsorption simulations.
- Can read mixture simulations
- Can read unfinished simulation data (reads the last cycle)

 >>> python read-raspa-output.py Output/System_0/output_IRMOF-1_1.1.1_298.000000_1e+07.data
"""
import os
import sys
import glob


def parse_output(data_file, verbose=False, save=False, loading='absolute'):
    """Parse output file for gas adsorption data.
    Args:
        data_file (str): path to RASPA simulation output file.
    Returns:
        results (dict): absolute and excess molar, gravimetric, and volumetric
            gas loadings, as well as energy of average, van der Waals, and
            Coulombic host-host, host-adsorbate, and adsorbate-adsorbate
            interactions.
    """
    with open(data_file) as ads_data:
        data_lines = ads_data.readlines()

    results = dict(ads={}, err={}, finished=False, warnings=[], components=[],
                   framework=os.path.basename(data_file).split('_')[1])
    for i, line in enumerate(data_lines):
        if 'Number of molecules:' in line:
            ads_start = i
        if 'Average Widom Rosenbluth factor:' in line:
            ads_end = i
        if 'Simulation finished' in line:
            results['finished'] = True
        if 'WARNING' in line:
            results['warnings'].append(line)
        if '(Adsorbate molecule)' in line:
            results['components'].append(line.split()[2].replace('[', '').replace(']', ''))
    if len(results['warnings']) > 0:
        print('%s - %i warning(s) found -> %s' %
              (results['name'], len(results['warnings']),
               results['warnings'][0].strip())) if verbose else None

    if results['finished']:
        ads_lines = data_lines[ads_start:ads_end]
        for i, line in enumerate(ads_lines):
            if 'Component' in line:
                comp_name = line.split()[2].replace('[', '').replace(']', '')
                results['ads'][comp_name] = {'id': line.split()[1]}
                results['err'][comp_name] = {'id': line.split()[1]}
            if 'Average loading %s [molecules/unit cell]' % loading in line:
                results['ads'][comp_name]['mol/uc'] = float(ads_lines[i].split()[5])
                results['err'][comp_name]['mol/uc'] = float(ads_lines[i].split()[7])

                results['ads'][comp_name]['mol/kg'] = float(ads_lines[i + 1].split()[5])
                results['err'][comp_name]['mol/kg'] = float(ads_lines[i + 1].split()[7])

                results['ads'][comp_name]['mg/g'] = float(ads_lines[i + 2].split()[5])
                results['err'][comp_name]['mg/g'] = float(ads_lines[i + 2].split()[7])

                results['ads'][comp_name]['cc/g'] = float(ads_lines[i + 3].split()[6])
                results['err'][comp_name]['cc/g'] = float(ads_lines[i + 3].split()[8])

                results['ads'][comp_name]['cc/cc'] = float(ads_lines[i + 4].split()[6])
                results['err'][comp_name]['cc/cc'] = float(ads_lines[i + 4].split()[8])
    else:
        results['initialization'], results['cycle'] = False, 0
        for i, line in enumerate(data_lines):
            if 'Current cycle' in line and line[0] == 'C':  # If production cycle
                results['cycle'] = int(line.split()[2])
                results['initialization'] = True
            if 'Loadings per component' in line and results['initialization']:
                for j, comp_name in enumerate(results['components']):
                    results['ads'][comp_name] = {'id': j}
                    results['ads'][comp_name]['mol/uc'] = float(data_lines[i + 3 + 6 * j].split()[2])
                    results['ads'][comp_name]['mol/kg'] = float(data_lines[i + 3 + 6 * j].split()[6])
                    results['ads'][comp_name]['mg/g'] = float(data_lines[i + 3 + 6 * j].split()[10])
                    results['ads'][comp_name]['cc/g'] = float(data_lines[i + 4 + 6 * j].split()[0])
                    results['ads'][comp_name]['cc/cc'] = float(data_lines[i + 4 + 6 * j].split()[5])
                    # Errors are not printed for unfinished simulations
                    results['err'][comp_name] = {'id': j}
                    results['err'][comp_name]['mol/uc'] = 0
                    results['err'][comp_name]['mol/kg'] = 0
                    results['err'][comp_name]['mg/g'] = 0
                    results['err'][comp_name]['cc/g'] = 0
                    results['err'][comp_name]['cc/cc'] = 0
        print('%s\nSimulation not finished!' % ('=' * 50))
        print('Initialization: %s | Last cycle: %i' % (results['initialization'], results['cycle']))

    if verbose:
        units = ['mol/uc', 'mg/g', 'cc/cc']
        for component in results['ads']:
            print('=' * 50)
            print("%-15s\t%s" % ('%s [%s]' % (component, results['ads'][component]['id']), loading))
            print('-' * 50)
            for u in units:
                print('%s\t\t%8.3f +/- %5.2f' % (u, results['ads'][component][u], results['err'][component][u]))
        print('=' * 50)

    if save:
        import yaml
        with open('raspa_ads.yaml', 'w') as rads:
            yaml.dump(results, rads)
    return results


if __name__ == "__main__":
    # ads_path = glob.glob(os.path.join(sys.argv[1], 'Output', 'System_0', '*.data'))[0]
    ads_path = os.path.abspath(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == 's':
        parse_output(ads_path, verbose=True, save=True)
    else:
        parse_output(ads_path, verbose=True, save=False)
