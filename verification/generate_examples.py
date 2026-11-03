"""Generate exact finite-spectrum examples and the time-resolution plot."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import random
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"]="spectral-memory-v1"
import matplotlib.pyplot as plt

from band_code import compile_band,dyadic_grid,nearest_integer,exact_spectrum,exact_occupancy


def main():
    out=Path(__file__).with_name("results");out.mkdir(exist_ok=True)
    figures=Path(__file__).parents[1]/"figures";figures.mkdir(exist_ok=True)
    n=16;eps=F(1,16);rng=random.Random(20261103)
    denominator=1<<40
    couplings=[F(rng.randrange(denominator,2*denominator),denominator) for _ in range(n)]
    spectrum=exact_spectrum(couplings)
    assert len(set(spectrum))==1<<n  # Exact rational distinctness check.
    rows=[]
    C=2+math.sqrt(2*math.pi)
    for root_time in [1,2,4,8,16]:
        t=F(root_time**2);delta=dyadic_grid(n,t,eps)
        estimates=[nearest_integer(g/delta)*delta for g in couplings]
        assert all(abs(g-h)<=delta/2 for g,h in zip(couplings,estimates))
        code=compile_band(estimates,t,eps,[delta/2]*n)
        M=exact_occupancy(spectrum,F(1,root_time))
        row=code.report();row.update(occupancy=M,unrestricted_qubit_upper=min(n,
            math.floor(math.log2(C*M/(1-float(eps))))),
            largest_bare_coherence=math.exp(-float(t)*float(min(couplings))**2/2))
        rows.append(row)
    data={"physical_qubits":n,"epsilon":str(eps),
          "couplings":[str(g) for g in couplings],"distinct_eigenvalues":len(set(spectrum)),
          "model":"A=sum_j g_j |1><1|_j; Gaussian kernel exp(-t gap^2/2)",
          "rows":rows}
    (out/"examples.json").write_text(json.dumps(data,indent=2)+"\n")
    t=[float(F(x['time'])) for x in rows]
    achieved=[x['logical_qubits'] for x in rows]
    upper=[x['unrestricted_qubit_upper'] for x in rows]
    fig,axes=plt.subplots(1,2,figsize=(10.6,4.2),layout="constrained")
    axes[0].plot(t,upper,"o--",color="#74889e",label="Converse upper bound")
    axes[0].plot(t,achieved,"o-",color="#135d9e",label="Compiled band code")
    axes[0].fill_between(t,achieved,upper,color="#dce8f3",alpha=.65)
    axes[0].set(xscale="log",xlabel="Storage time t (fixed noise units)",
                ylabel="Logical qubits",ylim=(0,n),title="Finite-time quantum storage")
    axes[0].set_xticks(t,[str(int(x)) for x in t]);axes[0].legend(frameon=False,fontsize=9)
    axes[1].plot(t,[x['largest_bare_coherence'] for x in rows],"o-",color="#b65b33")
    axes[1].set(xscale="log",yscale="log",xlabel="Storage time t (fixed noise units)",
                ylabel="Largest single-qubit coherence factor",title="Bare qubit coherence")
    axes[1].set_xticks(t,[str(int(x)) for x in t])
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.18)
    fig.suptitle("16 unequal couplings; all 65,536 eigenvalues distinct; error target 1/16",fontsize=12)
    fig.savefig(figures/"finite_time_memory.png",dpi=180)
    fig.savefig(figures/"finite_time_memory.svg",metadata={"Date":None})
    svg_path=figures/"finite_time_memory.svg"
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines())+"\n")
    plt.close(fig)
    print(json.dumps({"distinct_eigenvalues":data['distinct_eigenvalues'],"rows":rows},indent=2))


if __name__=="__main__":
    main()
