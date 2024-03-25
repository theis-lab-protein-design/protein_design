import torch
import esm


def esmfold(sequence : str):
    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda() 


    with torch.no_grad():
        output = model.infer_pdb(sequence)

    with open("result.pdb", "w") as f:
        f.write(output)

    import biotite.structure.io as bsio
    struct = bsio.load_structure("result.pdb", extra_fields=["b_factor"])
    print(struct.b_factor.mean())  


sequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
esmfold(sequence);