# Notes about writing more presets:
# ---------------------------------
# - all parameter names below are PLANCK parameter names. They are substituted by the
#   theory-code-specific ones in `create_input`
# - all presets below, either "atomic" (e.g. primordial, geometry...) or for full runs
#   must be OrderedDict's!
# - don't use extra_args for precision parameters! because if the same precision param
#   is mentioned twice at the same time in different fields with different values, there
#   is no facility to take the max (or min). Instead, codify precision needs in terms of
#   requirements in the .needs method of the cosmo code.

# Python 2/3 compatibility
from __future__ import absolute_import, division, print_function

# Global
from collections import OrderedDict as odict
from copy import deepcopy
import os

# Local
from cobaya.conventions import _theory, _params, _likelihood, _sampler, _prior, _p_derived
from cobaya.conventions import _p_ref, _p_proposal, _p_label, _p_dist, _p_drop, _p_value
from cobaya.conventions import _p_renames, _chi2, _separator

_camb = "camb"
_classy = "classy"
_desc = "desc"
_comment = "note"
_extra_args = "extra_args"
_error_msg = "error_msg"
_none = "(None)"

# Theory codes
theory = odict([[_camb, None], [_classy, None]])

# Primordial perturbations
primordial = odict([
    ["SFSR", {
        _desc: "Adiabatic scalar perturbations, power law spectrum",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["logA", odict([
                [_prior, odict([["min", 1.61], ["max", 3.91]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 3.05], ["scale", 0.001]])],
                [_p_proposal, 0.001], [_p_label, r"\log(10^{10} A_\mathrm{s})"],
                [_p_drop, True]])],
            ["As", odict([
                [_p_value, "lambda logA: 1e-10*np.exp(logA)"],
                [_p_label, r"A_\mathrm{s}"]])],
            ["ns", odict([
                [_prior, odict([["min", 0.8], ["max", 1.2]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.965], ["scale", 0.004]])],
                [_p_proposal, 0.002], [_p_label, r"n_\mathrm{s}"]])]])}]])
primordial.update(odict([
    ["SFSR_DESpriors", {
        _desc: "Adiabatic scalar perturbations, power law + running spectrum -- DESpriors",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["As_1e9", odict([
                [_prior, odict([["min", 0.5], ["max", 5]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 2.1], ["scale", 0.5]])],
                [_p_proposal, 0.25], [_p_label, r"10^9 A_\mathrm{s})"],
                [_p_drop, True], [_p_renames, "A"]])],
            ["As", odict([
                [_p_value, "lambda As_1e9: 1e-9 * As_1e9"],
                [_p_label, r"A_\mathrm{s}"]])],
            ["ns", primordial["SFSR"][_params]["ns"]]])}]]))
primordial.update(odict([
    ["SFSR_run", {
        _desc: "Adiabatic scalar perturbations, power law + running spectrum",
        _theory: {_camb: None, _classy: None},
        _params: odict(
            (list(primordial["SFSR"][_params].items()) +
             [["nrun", odict([
                 [_prior, odict([["min", -1], ["max", 1]])],
                 [_p_ref, odict([[_p_dist, "norm"], ["loc", 0], ["scale", 0.005]])],
                 [_p_proposal, 0.001], [_p_label, r"n_\mathrm{run}"]])]]))}]]))
primordial.update(odict([
    ["SFSR_runrun", {
        _desc: "Adiabatic scalar perturbations, power law + 2nd-order running spectrum",
        _theory: {_camb: None, _classy: None},
        _params: odict(
            (list(primordial["SFSR_run"][_params].items()) +
             [["nrunrun", odict([
                 [_prior, odict([["min", -1], ["max", 1]])],
                 [_p_ref, odict([[_p_dist, "norm"], ["loc", 0], ["scale", 0.002]])],
                 [_p_proposal, 0.001], [_p_label, r"n_\mathrm{run,run}"]])]]))}]]))
primordial.update(odict([
    ["SFSR_t", {
        _desc: "Adiabatic scalar+tensor perturbations, "
               "power law spectrum (inflation consistency)",
        _theory: {_camb: {_extra_args: {"nt": None}},
                  _classy: {_extra_args: {"n_t": "scc", "alpha_t": "scc"}}},
        _params: odict(
            (list(primordial["SFSR"][_params].items()) +
             [["r", odict([
                 [_prior, odict([["min", 0], ["max", 3]])],
                 [_p_ref, odict([[_p_dist, "norm"], ["loc", 0], ["scale", 0.03]])],
                 [_p_proposal, 0.03], [_p_label, r"r_{0.05}"]])]]))}]]))
primordial.update(odict([
    ["SFSR_t_nrun", {
        _desc: "Adiabatic scalar+tensor perturbations, "
               "power law + running spectrum (inflation consistency)",
        _theory: {_camb:
                      {_extra_args: primordial["SFSR_t"][_theory][_camb][_extra_args]},
                  _classy:
                      {_extra_args: primordial["SFSR_t"][_theory][_classy][_extra_args]}},
        _params: odict(
            (list(primordial["SFSR_run"][_params].items()) +
             list(primordial["SFSR_t"][_params].items())))}]]))

# Geometry
geometry = odict([
    ["flat", {
        _desc: "Flat FLRW universe",
        _theory: {_camb: None, _classy: None}}],
    ["omegak", {
        _desc: "FLRW model with varying curvature (prior on Omega_k)",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["omegak", odict([
                [_prior, odict([["min", -0.3], ["max", 0.3]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", -0.009], ["scale", 0.001]])],
                [_p_proposal, 0.001], [_p_label, r"\Omega_k"]])]])}], ])

# Hubble parameter constraints
H0_min, H0_max = 20, 100
hubble = odict([
    ["H", {
        _desc: "Hubble parameter",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["H0", odict([
                [_prior, odict([["min", H0_min], ["max", H0_max]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 67], ["scale", 2]])],
                [_p_proposal, 2], [_p_label, r"H_0"]])]])}],
    ["H_DESpriors", {
        _desc: "Hubble parameter (reduced range for DES and lensing-only constraints)",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["H0", odict([
                [_prior, odict([["min", 55], ["max", 91]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 67], ["scale", 2]])],
                [_p_proposal, 2], [_p_label, r"H_0"]])]])}],
    ["sound_horizon_last_scattering", {
        _desc: "Angular size of the sound horizon at last scattering "
               "(approximate, if using CAMB)",
        _theory: {
            _camb: {
                _params: odict([
                    ["theta_MC_100", odict([
                        [_prior, odict([["min", 0.5], ["max", 10]])],
                        [_p_ref,
                         odict([[_p_dist, "norm"], ["loc", 1.04109], ["scale", 0.0004]])],
                        [_p_proposal, 0.0002], [_p_label, r"100\theta_\mathrm{MC}"],
                        [_p_drop, True], [_p_renames, "theta"]])],
                    ["cosmomc_theta", odict([
                        [_p_value, "lambda theta_MC_100: 1.e-2*theta_MC_100"],
                        [_p_derived, False]])],
                    ["H0", {_p_label: r"H_0", "min": H0_min, "max": H0_max}]]),
                _extra_args: odict([["theta_H0_range", [H0_min, H0_max]]])},
            _classy: {
                _params: odict([
                    ["theta_s_1e2", odict([
                        [_prior, odict([["min", 0.5], ["max", 10]])],
                        [_p_ref, odict([
                            [_p_dist, "norm"], ["loc", 1.0416], ["scale", 0.0004]])],
                        [_p_proposal, 0.0002], [_p_label, r"100\theta_\mathrm{s}"],
                        [_p_drop, True]])],
                    ["100*theta_s", odict([
                        [_p_value, "lambda theta_s_1e2: theta_s_1e2"],
                        [_p_derived, False]])],
                    ["H0", {_p_label: r"H_0"}]])}}}]])

# Matter sector (minus light species)
N_eff_std = 3.046
nu_mass_fac = 94.0708
matter = odict([
    ["omegab_h2, omegac_h2", {
        _desc: "Flat prior on Omega*h^2 for barions and cold dark matter",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["omegabh2", odict([
                [_prior, odict([["min", 0.005], ["max", 0.1]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.0224], ["scale", 0.0001]])],
                [_p_proposal, 0.0001], [_p_label, r"\Omega_\mathrm{b} h^2"]])],
            ["omegach2", odict([
                [_prior, odict([["min", 0.001], ["max", 0.99]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.120], ["scale", 0.001]])],
                [_p_proposal, 0.0005], [_p_label, r"\Omega_\mathrm{c} h^2"]])],
            ["omegam", {_p_label: r"\Omega_\mathrm{m}"}]])}],
    ["Omegab, Omegam", {
        _desc: "Flat prior on Omega for barions and total matter",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["omegab", odict([
                [_prior, odict([["min", 0.03], ["max", 0.07]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.0495], ["scale", 0.004]])],
                [_p_proposal, 0.004], [_p_label, r"\Omega_\mathrm{b}"],
                [_p_drop, True]])],
            ["omegam", odict([
                [_prior, odict([["min", 0.1], ["max", 0.9]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.316], ["scale", 0.02]])],
                [_p_proposal, 0.02], [_p_label, r"\Omega_\mathrm{m}"],
                [_p_drop, True]])],
            ["omegabh2", odict([
                [_p_value, "lambda omegab, H0: omegab*(H0/100)**2"],
                [_p_label, r"\Omega_\mathrm{b} h^2"]])],
            ["omegach2", odict([
                [_p_value, ("lambda omegam, omegab, mnu, H0: "
                            "(omegam-omegab)*(H0/100)**2-(mnu*(%g/3)**0.75)/%g" % (
                                N_eff_std, nu_mass_fac))],
                [_p_label, r"\Omega_\mathrm{c} h^2"]])]
        ])}]])
for m in matter.values():
    m[_params]["omegamh2"] = odict([
        [_p_derived, "lambda omegam, H0: omegam*(H0/100)**2"],
        [_p_label, r"\Omega_\mathrm{m} h^2"]])

# Neutrinos and other extra matter
neutrinos = odict([
    ["one_heavy_planck", {
        _desc: "Two massless nu and one with m=0.06. Neff=3.046",
        _theory: {
            _camb: {_extra_args: {"num_massive_neutrinos": 1, "nnu": 3.046},
                    _params: odict([["mnu", 0.06]])},
            _classy: {_extra_args: {"N_ncdm": 1, "N_ur": 2.0328},
                      _params: odict([
                          ["m_ncdm", {_p_value: 0.06, _p_renames: "mnu"}]])}}}],
    ["varying_mnu", {
        _desc: "Varying total mass of 3 degenerate nu's, with N_eff=3.046",
        _theory: {
            _camb: {_extra_args: {"num_massive_neutrinos": 3, "nnu": 3.046},
                    _params: odict([
                        ["mnu", odict([
                            [_prior, odict([["min", 0], ["max", 5]])],
                            [_p_ref, odict([
                                [_p_dist, "norm"], ["loc", 0.02], ["scale", 0.1]])],
                            [_p_proposal, 0.03], [_p_label, r"\sum m_\nu"]])]])},
            _classy: {_extra_args: {"N_ncdm": 1, "deg_ncdm": 3, "N_ur": 0.00641},
                      _params: odict([
                          ["m_ncdm", odict([
                              [_prior, odict([["min", 0], ["max", 1.667]])],
                              [_p_ref, odict([
                                  [_p_dist, "norm"], ["loc", 0.0067], ["scale", 0.033]])],
                              [_p_proposal, 0.01], [_p_label, r"m_\nu"]])],
                          ["mnu", odict([[_p_derived, "lambda m_ncdm: 3 * m_ncdm"],
                                         [_p_label, r"\sum m_\nu"]])]])}}}],
    ["varying_Neff", {
        _desc: "Varying Neff with two massless nu and one with m=0.06",
        _theory: {
            _camb: {_extra_args: {"num_massive_neutrinos": 1},
                    _params: odict([
                        ["mnu", 0.06],
                        ["nnu", odict([
                            [_prior, odict([["min", 0.05], ["max", 10]])],
                            [_p_ref, odict([
                                [_p_dist, "norm"], ["loc", 3.046], ["scale", 0.05]])],
                            [_p_proposal, 0.05], [_p_label, r"N_\mathrm{eff}"]])]])},
            _classy: {_extra_args: {"N_ncdm": 1},
                      _params: odict([
                          ["m_ncdm", odict([[_p_value, 0.06], [_p_renames, "mnu"]])],
                          ["N_ur", odict([
                              [_prior, odict([["min", 0.0001], ["max", 9]])],
                              [_p_ref, odict([
                                  [_p_dist, "norm"], ["loc", 2.0328], ["scale", 0.05]])],
                              [_p_proposal, 0.05], [_p_label, r"N_\mathrm{ur}"]])],
                          ["nnu", odict([
                              [_p_derived, "lambda Neff: Neff"],
                              [_p_label, r"N_\mathrm{eff}"]])]])}}}]])
neutrinos.update(odict([
    ["varying_mnu_Neff", {
        _desc: "Varying Neff and total mass of 3 degenerate nu's",
        _theory: {
            _camb: {
                _extra_args: {"num_massive_neutrinos": 3},
                _params: odict([
                    ["mnu", deepcopy(
                        neutrinos["varying_mnu"][_theory]["camb"][_params]["mnu"])],
                    ["nnu", deepcopy(
                        neutrinos["varying_Neff"][_theory]["camb"][_params]["nnu"])]])},
            #            _classy: {
            #                _extra_args: {"N_ncdm": 1, "deg_ncdm": 3},
            #                _params: odict([
            #                    ["m_ncdm", deepcopy(
            #                        neutrinos["varying_mnu"][_theory]["classy"][_params]["m_ncdm"])],
            #                    ["mnu", deepcopy(
            #                        neutrinos["varying_mnu"][_theory]["classy"][_params]["mnu"])],
            #                    ["N_ur", deepcopy(
            #                        neutrinos["varying_Neff"][_theory]["classy"][_params]["N_ur"])],
            #                    ["nnu", deepcopy(
            #                        neutrinos["varying_Neff"][_theory]["classy"][_params]["nnu"])]
            #                ])}
        }}]]))
# neutrinos["varying_mnu_Neff"][_theory][_classy][_params]["N_ur"][_p_ref]["loc"] = 0.00641

#    # ["varying_Neff+1sterile", {
#    #     _desc: "Varying Neff plus 1 sterile neutrino (SM nu's with m=0,0,0.06)",
#    #     _theory: {
#    #         _camb: {_extra_args: odict(
#    #             list(neutrinos["varying_Neff"][_theory][_camb][_extra_args].items()) +
#    #             [["accuracy_level", 1.2]])}},
#    #     _params: odict([
#    #         ["nnu", odict([
#    #             [_prior, odict([["min", 3.046], ["max", 10]])],
#    #             [_p_ref, odict([[_p_dist, "norm"], ["loc", 3.046], ["scale", 0.05]])],
#    #             [_p_proposal, 0.05], [_p_label, r"N_\mathrm{eff}"]])],
#    #         ["meffsterile", odict([
#    #             [_prior, odict([["min", 0], ["max", 3]])#,
#    #             [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.1], ["scale", 0.1]])],
#    #             [_p_proposal, 0.03],
#    #             [_p_label, r"m_{\nu,\mathrm{sterile}}^\mathrm{eff}"]])]])}]

# Dark Energy
dark_energy = odict([
    ["lambda", {
        _desc: "Cosmological constant (w=-1)",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["omegal", {_p_label: r"\Omega_\Lambda"}]])}],
    ["de_w", {
        _desc: "Varying constant eq of state",
        _theory: {_camb: None,
                  _classy: {_params: {"Omega_Lambda": 0}}},
        _params: odict([
            ["w", odict([
                [_prior, odict([["min", -3], ["max", -0.333]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", -0.99], ["scale", 0.02]])],
                [_p_proposal, 0.02], [_p_label, r"w_\mathrm{DE}"]])]])}],
    ["de_w_wa", {
        _desc: "Varying constant eq of state with w(a) = w0 + (1-a) wa",
        _theory: {_camb: None,
                  _classy: {_params: {"Omega_Lambda": 0}}},
        _params: odict([
            ["w", odict([
                [_prior, odict([["min", -3], ["max", 1]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", -0.99], ["scale", 0.02]])],
                [_p_proposal, 0.02], [_p_label, r"w_{0,\mathrm{DE}}"]])],
            ["wa", odict([
                [_prior, odict([["min", -3], ["max", 2]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0], ["scale", 0.05]])],
                [_p_proposal, 0.05], [_p_label, r"w_{a,\mathrm{DE}}"]])]])}]])

# BBN
bbn_derived_camb = odict([
    ["YpBBN", odict([[_p_label, r"Y_P^\mathrm{BBN}"]])],
    ["DHBBN", odict([[_p_derived, r"lambda DH: 10**5*DH"],
                     [_p_label, r"10^5 \mathrm{D}/\mathrm{H}"]])]])
bbn = odict([
    ["consistency", {
        _desc: "Primordial Helium fraction inferred from BBN consistency",
        _theory: {_camb: {_params: bbn_derived_camb},
                  _classy: None},
        _params: odict([
            ["yheused", {_p_label: r"Y_\mathrm{P}"}]])}],
    ["YHe_des_y1", {
        _desc: "Fixed Y_P = 0.245341 (used in DES Y1)",
        _theory: {_camb: None,
                  _classy: None},
        _params: odict([
            ["yhe", 0.245341]])}],
    ["YHe", {
        _desc: "Varying primordial Helium fraction",
        _theory: {_camb: None,
                  _classy: None},
        _params: odict([
            ["yhe", odict([
                [_prior, odict([["min", 0.1], ["max", 0.5]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.237], ["scale", 0.006]])],
                [_p_proposal, 0.006], [_p_label, r"Y_\mathrm{P}"]])]])}], ])

# Reionization
reionization = odict([
    ["std", {
        _desc: "Standard reio, lasting delta_z=0.5",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["tau", odict([
                [_prior, odict([["min", 0.01], ["max", 0.8]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.055], ["scale", 0.006]])],
                [_p_proposal, 0.003], [_p_label, r"\tau_\mathrm{reio}"]])],
            ["zrei", {_p_label: r"z_\mathrm{re}"}]])}],
    ["gauss_prior", {
        _desc: "Standard reio, lasting delta_z=0.5, gaussian prior around tau=0.07",
        _theory: {_camb: None, _classy: None},
        _params: odict([
            ["tau", odict([
                [_prior, odict([[_p_dist, "norm"], ["loc", 0.07], ["scale", 0.02]])],
                [_p_ref, odict([[_p_dist, "norm"], ["loc", 0.07], ["scale", 0.01]])],
                [_p_proposal, 0.005], [_p_label, r"\tau_\mathrm{reio}"]])],
            ["zrei", {_p_label: r"z_\mathrm{re}"}]])}],
    ["irrelevant", {
        _desc: "Irrelevant (NB: only valid for non-CMB or CMB-marged datasets!)",
        _theory: {_camb: None, _classy: None},
        _params: odict([])}], ])

# EXPERIMENTS ############################################################################
cmb_precision = {_camb: {"halofit_version": "mead",
                         "bbn_predictor": "PArthENoPE_880.2_standard.dat",
                         "lens_potential_accuracy": 1},
                 _classy: {"non linear": "halofit"}}
cmb_sampler_recommended = {"mcmc": {"drag": True, "proposal_scale": 1.9}}

like_cmb = odict([
    [_none, {}],
    ["planck_2018", {
        _desc: "Planck 2018 (Polarized CMB + lensing)",
        _comment: None,
        _sampler: cmb_sampler_recommended,
        _theory: {theo: {_extra_args: cmb_precision[theo]}
                  for theo in [_camb, _classy]},
        _likelihood: odict([
            ["planck_2018_lowl.TT", None],
            ["planck_2018_lowl.EE", None],
            ["planck_2018_highl_plik.TTTEEE", None],
            ["planck_2018_lensing.clik", None]])}],
    ["planck_2018_bk15", {
        _desc: "Planck 2018 (Polarized CMB + lensing) + Bicep/Keck-Array 2015",
        _sampler: cmb_sampler_recommended,
        _theory: {theo: {_extra_args: cmb_precision[theo]}
                  for theo in [_camb, _classy]},
        _likelihood: odict([
            ["planck_2018_lowl.TT", None],
            ["planck_2018_lowl.EE", None],
            ["planck_2018_highl_plik.TTTEEE", None],
            ["planck_2018_lensing.clik", None],
            ["bicep_keck_2015", None]])}],
    ["planck_2018_CMBmarged_lensing", {
        _desc: "Planck 2018 CMB-marginalized lensing",
        _sampler: cmb_sampler_recommended,
        _theory: {theo: {_extra_args: cmb_precision[theo]}
                  for theo in [_camb, _classy]},
        _likelihood: odict([
            ["planck_2018_lensing.cmbmarged", None]])}],
])
like_cmb["planck_2018_bk15"][_comment] = like_cmb["planck_2018"][_comment]
# Add common CMB derived parameters
for name, m in like_cmb.items():
    # Don't add the derived parameter to the no-CMB case!
    if not m:
        continue
    if _params not in m:
        m[_params] = odict()
    m[_params].update(odict([
        ["sigma8", {_p_label: r"\sigma_8"}],
        ["s8h5", odict([
            [_p_derived, "lambda sigma8, H0: sigma8*(H0*1e-2)**(-0.5)"],
            [_p_label, r"\sigma_8/h^{0.5}"]])],
        ["s8omegamp5", odict([
            [_p_derived, "lambda sigma8, omegam: sigma8*omegam**0.5"],
            [_p_label, r"\sigma_8 \Omega_\mathrm{m}^{0.5}"]])],
        ["s8omegamp25", odict([
            [_p_derived, "lambda sigma8, omegam: sigma8*omegam**0.25"],
            [_p_label, r"\sigma_8 \Omega_\mathrm{m}^{0.25}"]])],
        ["A", odict([
            [_p_derived, "lambda As: 1e9*As"],
            [_p_label, r"10^9 A_\mathrm{s}"]])],
        ["clamp", odict([
            [_p_derived, "lambda As, tau: 1e9*As*np.exp(-2*tau)"],
            [_p_label, r"10^9 A_\mathrm{s} e^{-2\tau}"]])],
        ["age", odict([
            [_p_label, r"{\rm{Age}}/\mathrm{Gyr}"]])],
        ["rdrag", odict([
            [_p_label, r"r_\mathrm{drag}"]])]]))
    if "cmbmarged" in name.lower():
        m[_params].pop("A")
        m[_params].pop("clamp")
# Some more, in case we want to add them at some point, described in
# https://wiki.cosmos.esa.int/planckpla2015/images/b/b9/Parameter_tag_definitions_2015.pdf
#    "zstar":       {"latex": r"z_*"},
#    "rstar":       {"latex": r"r_*"},
#    "thetastar":   {"latex": r"100\theta_*"},
#    "DAstar":      {"latex": r"D_\mathrm{A}/\mathrm{Gpc}"},
#    "zdrag":       {"latex": r"z_\mathrm{drag}"},
#    "kd":          {"latex": r"k_\mathrm{D}"},
#    "thetad":      {"latex": r"100\theta_\mathrm{D}"},
#    "zeq":         {"latex": r"z_\mathrm{eq}"},
#    "keq":         {"latex": r"k_\mathrm{eq}"},
#    "thetaeq":     {"latex": r"100\theta_\mathrm{eq}"},
#    "thetarseq":   {"latex": r"100\theta_\mathrm{s,eq}"},
for combination, info in like_cmb.items():
    if info:
        likes = ", ".join([_chi2 + _separator + like.replace(".", "_")
                           for like in info[_likelihood]])
        info[_params].update(odict([
            ["chi2__CMB", odict([[_p_derived, "lambda %s: sum([%s])" % (likes, likes)],
                                 [_p_label, r"\chi^2_\mathrm{CMB}"]])]]))

like_bao = odict([
    [_none, {}],
    ["BAO_planck_2018", {
        _desc: "Baryon acoustic oscillation data from DR12, MGS and 6DF",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["bao.sixdf_2011_bao", None],
            ["bao.sdss_dr7_mgs", None],
            ["bao.sdss_dr12_consensus_bao", None]])}],
])
for combination, info in like_bao.items():
    if info:
        likes = ", ".join([_chi2 + _separator + like.replace(".", "_")
                           for like in info[_likelihood]])
        info[_params] = odict([
            ["chi2__BAO", odict([[_p_derived, "lambda %s: sum([%s])" % (likes, likes)],
                                 [_p_label, r"\chi^2_\mathrm{BAO}"]])]])

like_des = odict([
    [_none, {}],
    ["des_y1_clustering", {
        _desc: "Galaxy clustering from DES Y1",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["des_y1.clustering", None]])}],
    ["des_y1_galaxy_galaxy", {
        _desc: "Galaxy-galaxy lensing from DES Y1",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["des_y1.galaxy_galaxy", None]])}],
    ["des_y1_shear", {
        _desc: "Cosmic shear data from DES Y1",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["des_y1.shear", None]])}],
    ["des_y1_joint", {
        _desc: "Combination of galaxy clustering and weak lensing data from DES Y1",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["des_y1.joint", None]])}],
])

like_sn = odict([
    [_none, {}],
    ["Pantheon", {
        _desc: "Supernovae data from the Pantheon sample",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["sn.pantheon", None]])}],
])

like_H0 = odict([
    [_none, {}],
    ["Riess2018a", {
        _desc: "Local H0 measurement from Riess et al. 2018a (used in Planck 2018)",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["H0.riess2018a", None]])}],
    ["Riess201903", {
        _desc: "Local H0 measurement from Riess et al. 2019",
        _theory: {_camb: None, _classy: None},
        _likelihood: odict([
            ["H0.riess201903", None]])}],
])

# SAMPLERS ###############################################################################

sampler = odict([
    ["MCMC", {
        _desc: "MCMC sampler with covmat learning",
        _sampler: {"mcmc": {"covmat": "auto"}}}],
    ["PolyChord", {
        _desc: "Nested sampler, affine invariant and multi-modal",
        _sampler: {"polychord": None}}], ])

# PRESETS ################################################################################

planck_base_model = {
    "primordial": "SFSR",
    "geometry": "flat",
    "hubble": "sound_horizon_last_scattering",
    "matter": "omegab_h2, omegac_h2",
    "neutrinos": "one_heavy_planck",
    "dark_energy": "lambda",
    "bbn": "consistency",
    "reionization": "std"}
default_sampler = {"sampler": "MCMC"}

preset = odict([
    [_none, {_desc: "(No preset chosen)"}],
    # Pure CMB #######################################################
    ["planck_2018_camb", {
        _desc: "Planck 2018 with CAMB",
        "theory": _camb,
        "like_cmb": "planck_2018"}],
    ["planck_2018_classy", {
        _desc: "Planck 2018 with CLASS",
        "theory": _classy,
        "like_cmb": "planck_2018"}],
    ["planck_2018_bicep_camb", {
        _desc: "Planck 2018 + BK15 (with tensor modes) with CAMB",
        "theory": _camb,
        "primordial": "SFSR_t",
        "like_cmb": "planck_2018_bk15"}],
    ["planck_2018_bicep_classy", {
        _desc: "Planck 2018 + BK15 (with tensor modes) with CLASS",
        "theory": _classy,
        "primordial": "SFSR_t",
        "like_cmb": "planck_2018_bk15"}],
    # CMB+BAO ######################################################
    ["planck_2018_BAO_camb", {
        _desc: "Planck 2018 + BAO with CAMB",
        "theory": _camb,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018"}],
    ["planck_2018_BAO_classy", {
        _desc: "Planck 2018 + BAO with CLASS",
        "theory": _classy,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018"}],
    # CMB+BAO+SN ###################################################
    ["planck_2018_BAO_SN_camb", {
        _desc: "Planck 2018 + BAO + SN with CAMB",
        "theory": _camb,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018",
        "like_sn": "Pantheon"}],
    ["planck_2018_BAO_SN_classy", {
        _desc: "Planck 2018 + BAO + SN with CLASS",
        "theory": _classy,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018",
        "like_sn": "Pantheon"}],
    # CMB+DES+BAO+SN ###################################################
    ["planck_2018_DES_BAO_SN_camb", {
        _desc: "Planck 2018 + DESjoint + BAO + SN with CAMB",
        "theory": _camb,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018",
        "like_des": "des_y1_joint",
        "like_sn": "Pantheon"}],
    ["planck_2018_DES_BAO_SN_classy", {
        _desc: "Planck 2018 + DESjoint + BAO + SN with CLASS",
        "theory": _classy,
        "like_cmb": "planck_2018",
        "like_bao": "BAO_planck_2018",
        "like_des": "des_y1_joint",
        "like_sn": "Pantheon"}],
])

# Add planck baseline model
for pre in preset.values():
    pre.update(
        {field: value for field, value in planck_base_model.items() if field not in pre})
    pre.update(default_sampler)

# Lensing-only ###################################################
preset.update(odict([
    [_none, {_desc: "(No preset chosen)"}],
    ["planck_2018_DES_lensingonly_camb", {
        _desc: "Planck 2018 + DES Y1 lensing-only with CAMB",
        "theory": _camb,
        "like_cmb": "planck_2018_CMBmarged_lensing",
        "like_des": "des_y1_shear"}],
    ["planck_2018_DES_lensingonly_classy", {
        _desc: "Planck 2018 + DES Y1 lensing-only with CLASS",
        "theory": _classy,
        "like_cmb": "planck_2018_CMBmarged_lensing",
        "like_des": "des_y1_shear"}],
]))

lensingonly_model = {
    "primordial": "SFSR_DESpriors",
    "geometry": "flat",
    "hubble": "H_DESpriors",
    "matter": "Omegab, Omegam",
    "neutrinos": "one_heavy_planck",
    "dark_energy": "lambda",
    "bbn": "YHe_des_y1",
    "reionization": "irrelevant"}

# Add planck baseline model
for name, pre in preset.items():
    if "lensingonly" in name:
        pre.update(
            {field: value for field, value in lensingonly_model.items() if field not in pre})
        pre.update(default_sampler)

# BASIC INSTALLATION ######################################################################
install_basic = {
    _theory: {_camb: None, _classy: None},
    _likelihood: {
        "planck_2018_lowl.TT": None,
        "planck_2018_lensing.native": None,
        "bicep_keck_2015": None,
        "sn.pantheon": None,
        "bao.sdss_dr12_consensus_final": None,
        "des_y1.joint": None}}


install_tests = deepcopy(install_basic)
install_tests[_likelihood].update({"planck_2015_lowl": None,
                                   "planck_2018_highl_plik.TT_unbinned": None,
                                   "planck_2018_highl_plik.TT_lite_native": None,
                                   "planck_2018_highl_CamSpec.TT": None,
                                   "planck_2018_highl_CamSpec.TT_native": None,
})

skip_list = os.environ.get("COBAYA_TEST_SKIP", "").replace(",", " ").lower().split()
for key in list(install_tests.keys()):
    if any(skip for skip in skip_list if skip in key.lower()):
        skip_list.pop(key)
