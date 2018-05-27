"""
Read RASPA output file for mixture gas adsorption simulations.
"""
import os
import sys
import glob


def parse_output(data_file, verbose=True, save=False):
    """Parse output file for single or mixture gas adsorption data.
    Args:
        data_file (str): path to RASPA simulation output file.
        verbose (bool): Print results
        save (bool): Save results to a yaml file
    """
    with open(data_file) as ads_data:
        data_lines = ads_data.readlines()
    finished = False
    for i, line in enumerate(data_lines):
        if 'Number of molecules:' in line:
            ads_start = i
        if 'Average Widom Rosenbluth factor:' in line:
            ads_end = i
        if 'Simulation finished' in line:
            finished = True

    if finished:
        results = {}
        ads_lines = data_lines[ads_start:ads_end]
        for i, line in enumerate(ads_lines):
            if 'Component' in line:
                comp_name = line.split()[2].replace('[', '').replace(']', '')
                results[comp_name] = {'id': line.split()[1]}
            if 'Average loading absolute [molecules/unit cell]' in line:
                results[comp_name]['mol/uc'] = float(ads_lines[i].split()[5])
                results[comp_name]['mol/kg'] = float(ads_lines[i + 1].split()[5])
                results[comp_name]['mg/g'] = float(ads_lines[i + 2].split()[5])
                results[comp_name]['cc/g'] = float(ads_lines[i + 3].split()[6])
                results[comp_name]['cc/cc'] = float(ads_lines[i + 4].split()[6])
        if verbose:
            units = ['mol/uc', 'mg/g', 'cc/cc']
            for component in results:
                print("%s\n%-15s\tabsolute\n%s" % ('=' * 30, '%s [%s]' % (component, results[component]['id']), '-' * 30))
                for u in units:
                    print('%s\t\t%8.3f' % (u, results[component][u]))
            print('=' * 30)
        if save:
            import yaml
            with open('raspa_ads.yaml', 'w') as rads:
                yaml.dump(results, rads)
    else:
        print('Simulation not finished!')


if __name__ == "__main__":
    ads_path = glob.glob(os.path.join(sys.argv[1], 'Output', 'System_0', '*.data'))[0]
    if len(sys.argv) > 2 and sys.argv[2] == 's':
        parse_output(ads_path, verbose=True, save=True)
    else:
        parse_output(ads_path, verbose=True, save=False)
