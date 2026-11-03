"""Reproduce the finite checks supporting the spectral memory account.

Analytical proofs establish the uniform statements. These checks stress
finite arithmetic, signed/zero couplings, closed intervals, reference-stable
channel formulas and the implemented reversible encoder.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import random
import numpy as np

from band_code import compile_band, dyadic_grid, exact_occupancy, exact_spectrum
from verify_reversible_encoder import run_verification


def gaussian_checks():
    rng=np.random.default_rng(20261103)
    spectra=[("scalar",np.zeros(16)),("lattice",np.arange(32,dtype=float)),
      ("clusters",np.r_[np.linspace(0,.1,13),np.linspace(10,10.1,19)]),
      ("multiplicity",np.repeat(np.arange(7),[1,2,4,8,5,3,1])),
      ("irregular",np.sort(rng.normal(size=48)))]
    rows=[]
    for name,values in spectra:
        for t in [.001,.1,1.,100.]:
            G=np.exp(-t*(values[:,None]-values[None,:])**2/2)
            eig=np.linalg.eigvalsh(G)
            ordered=sorted(values)
            M=int(max(sum(x<=y<=x+1/math.sqrt(t)+1e-12 for y in ordered)
                      for x in ordered))
            cp_gap=float(np.linalg.eigvalsh(eig[-1]*np.eye(len(values))-G)[0])
            bound=(2+math.sqrt(2*math.pi))*M
            assert eig[0]>=-1e-10 and cp_gap>=-1e-10
            assert eig[-1]<=max(G.sum(axis=1))+1e-10<=bound+1e-10
            rows.append(dict(case=name,dimension=len(values),time=t,occupancy=M,
                             kernel_norm=float(eig[-1]),upper=bound,cp_residual=cp_gap))
    return rows


def exact_band_checks():
    rng=random.Random(20261103)
    rows=[]
    for n in range(1,11):
        for case in range(12):
            t=F([1,4,16][case%3]);eps=F(1,[16,64][case%2])
            delta=dyadic_grid(n,t,eps)
            target=eps/(16*n*n*t)
            assert delta*delta<=target<4*delta*delta
            if case==0:
                true=[F(0)]*n
            elif case==1:
                true=[delta/4*(-1 if j%2 else 1) for j in range(n)]
            else:
                true=[F(rng.randrange(-24,25),16) for _ in range(n)]
            estimates=[g+(-1 if j%2 else 1)*delta/2 for j,g in enumerate(true)]
            code=compile_band(estimates,t,eps,[delta/2]*n)
            assert code.storage_error_bound<=9*eps/16
            words=list(product((0,1),repeat=n))
            rounded=[sum(q*x for q,x in zip(code.signed_weights,w)) for w in words]
            lower=code.lower+code.origin;upper=code.upper+code.origin
            selected=[w for w,s in zip(words,rounded) if lower<=s<=upper]
            brute_best=max(sum(a<=s<=a+4*n for s in rounded) for a in set(rounded))
            assert len(selected)==code.population==brute_best
            selected.sort(key=lambda w:tuple(1-x if q<0 else x
                                             for x,q in zip(w,code.signed_weights)))
            for index,word in enumerate(selected):
                assert code.unrank(index)==word and code.rank(word)==index
            energies=[sum(g*x for g,x in zip(true,w)) for w in selected]
            assert max(energies)-min(energies)<=code.true_width_bound
            M=exact_occupancy(exact_spectrum(true),F(1,math.isqrt(t.numerator)))
            # Here epsilon is 1/(a perfect square), so k is exact.
            k=4*math.isqrt(eps.denominator)
            assert code.population>=(M+k-1)//k
            rows.append(dict(n=n,case=case,time=str(t),epsilon=str(eps),
                 grid=str(delta),occupancy=M,population=code.population,
                 logical_qubits=code.logical_qubits,enumerated_words=len(words)))
    return rows


def main():
    kernel=gaussian_checks();bands=exact_band_checks()
    output=Path(__file__).with_name("results")/"checks.json"
    output.parent.mkdir(exist_ok=True)
    # Mandatory gate-level verification.  Import failures and failed gate,
    # cleanup, reference-channel or independent-compiler checks abort the run.
    gates=run_verification(output.parent)
    assert gates["all_passed"]
    circuit_cases=gates["cases"]
    gate_summary={
        "status":"pass",
        "result_file":"reversible_encoder.json",
        "primitive_gate_file":"signed_zero_n4_primitive_gates.json",
        "exact_rational_checks":gates["arithmetic"]["exact_rational_checks"],
        "circuit_cases":len(circuit_cases),
        "logical_basis_inputs_checked":sum(x["dimension"] for x in circuit_cases),
        "independent_band_words_compared":sum(
            x["primary_module_comparison"]["accepted_words_ranked_and_unranked"]
            for x in circuit_cases),
        "independent_completion_addresses_compared":sum(
            x["primary_module_comparison"]["completion_table_addresses_compared"]
            for x in circuit_cases),
        "max_encoder_primitive_gates":max(x["encoder_primitive_gate_count"] for x in circuit_cases),
        "max_temporary_work_qubits":max(x["temporary_work_qubits"] for x in circuit_cases),
        "max_decoded_schur_entry_error":max(
            x[test]["decoded_schur_max_entry_error"]
            for x in circuit_cases for test in ("bell_reference_test","generic_reference_test")),
        "all_encoder_and_decoder_workspaces_clean":all(
            x[test]["all_encoder_and_decoder_workspaces_clean"]
            for x in circuit_cases for test in ("bell_reference_test","generic_reference_test")),
        "boundary_cases":len(gates["boundary_checks"]["cases"]),
        "boundary_logical_basis_inputs_checked":gates["boundary_checks"]["logical_basis_inputs_checked"],
        "boundary_checks_passed":gates["boundary_checks"]["all_passed"],
    }
    result={"status":"pass","gaussian_kernel_cases":kernel,
            "exact_band_cases":bands,
            "gate_level_check":gate_summary,
            "limits":["Finite checks do not prove the all-spectrum theorem.",
                      "The supplied calibration certificates are inputs, not simulated experiments.",
                      "No hardware gate-noise or fault-tolerance claim is tested."]}
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","kernel_cases":len(kernel),
                     "exact_band_cases":len(bands),
                     "enumerated_words":sum(x['enumerated_words'] for x in bands),
                     "min_cp_residual":min(x['cp_residual'] for x in kernel),
                     "gate_level_check":gate_summary,
                     "result_path":str(output)},indent=2))


if __name__=="__main__":
    main()
