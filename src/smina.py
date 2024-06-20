def read_pdb_with_ob(file):
    """Read a molecule file with open babel

    Args:
        infile (Union[str os.PathLike]): input file

    Returns:
        mols (list): list of molecules found in the input file
    """

    try:
        from openbabel import pybel
    except ImportError:
        raise ImportError("Pybel is required for reading openbabel molecules")
    mols = [m for m in pybel.readfile(format="pdb",filename=str(file))]
    return mols 

def prepare_ob_mols(ligand, outpath, overwrite=False):
    from openbabel import pybel
    out = pybel.Outputfile(format="pdbqt" , filename=str(outpath),  overwrite=overwrite)
    ligand.addh()
    if not ligand.OBMol.HasNonZeroCoords():
        ligand.make3D()
    ligand.calccharges(model="gasteiger")
    out.write(ligand)
    out.close()

def get_protein_ligand_idxs(traj ,resname=None):
    protein = traj.top.select("protein")
    resname = "not protein and not water" if not resname else resname
    ligand = traj.top.select(resname)
    return protein, ligand

def save_trimmed_pdb(path, traj, idxs):
    traj.atom_slice(idxs).save_pdb(path)
