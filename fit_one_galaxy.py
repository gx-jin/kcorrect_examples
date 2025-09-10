# fit_one_galaxy.py
import sys
import kcorrect
import numpy as np
import json

def get_sed(kc, coeffs_obj,
            n_galaxy_templates=57600,
            n_agn_templates=36,):
    coeffs_galaxy = coeffs_obj[:n_galaxy_templates]
    coeffs_agn = coeffs_obj[n_galaxy_templates:n_galaxy_templates+n_agn_templates]
    templates_galaxy = kc.templates.flux[:n_galaxy_templates, :]
    templates_agn = kc.templates.flux[n_galaxy_templates:n_galaxy_templates+n_agn_templates, :]
    
    lam_rest = kc.templates.wave  # rest-frame wavelength (Angstrom)
    sed_galaxy = coeffs_galaxy @ templates_galaxy
    sed_agn = coeffs_agn @ templates_agn
    cut_6um = (lam_rest>5e4) & (lam_rest<6e4)
    fagn = np.nanmedian(sed_agn[cut_6um]) / (np.nanmedian(sed_galaxy[cut_6um]) + np.nanmedian(sed_agn[cut_6um]))
    fagn = 0 if not (fagn>0) else fagn

    return lam_rest, sed_galaxy, sed_agn, fagn

def get_smass(kc, coeffs_obj, z, corr_ld):
    derived = kc.derived(redshift=z, coeffs=coeffs_obj)
    smass = np.log10(derived['mremain'])-9.0 + 2*np.log10(corr_ld)
    b50 = derived['b50']
    b300 = derived['b300']
    b1000 = derived['b1000']
    metallicity = derived['metallicity']
    return smass, b50, b300, b1000, metallicity

if __name__ == '__main__':
    try:
        input_json_string = sys.stdin.read()
        input_data = json.loads(input_json_string)

        z = input_data['z']
        maggies = np.array(input_data['maggies'])
        ivar = np.array(input_data['ivar'])
        corr_ld = input_data['corr_ld']
        output_file = input_data['output_file']
        
        kc = kcorrect.kcorrect.Kcorrect(filename=input_data['kc_path'])

        coeffs = kc.fit_coeffs(
                    redshift=z,
                    maggies=maggies,
                    ivar=ivar
                )
        lam_rest, sed_galaxy, sed_agn, fagn = get_sed(kc, coeffs)
        smass, b50, b300, b1000, metallicity = get_smass(kc, coeffs, z, corr_ld)

        output_data = {
            "lam_rest": lam_rest,
            "sed_galaxy": sed_galaxy,
            "sed_agn": sed_agn,
            "fagn": fagn,
            "smass": smass,
            "b50": b50,
            "b300": b300,
            "b1000": b1000,
            "metallicity": metallicity,
            "nanomaggies": maggies,
            "ivars": ivar,
            "z": z
        }
        np.savez_compressed(output_file, **output_data)
    except Exception as e:
        print(f"Error during fitting: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
