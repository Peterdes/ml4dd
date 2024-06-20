# %% [markdown]
# Imports

# %%
import sys
sys.path.append('..')
import mdtraj

from src.workshop_2_utils import *

from config import settings

# %% [markdown]
# Hyperparameters for smina

# %%
# smina parameters
num_poses = 1
exhaustiveness = 8

# %% [markdown]
# Paths to set

# %%
# How many molecules we want to stuff for
num_mols = None

data_path = settings.data_path / "KIT_wt"

# prepared_protein_pdb_file = data_path / "6vhn_prepared.pdb"
prepared_protein_pdb_file = None
ligand_pdb_file = data_path / "ligand.pdb"

protein_pdbqt_file = data_path / "protein.pdbqt"

save_df_file = data_path / "poses.csv"

# %%

smina_inputs_path = data_path / "smina_inputs"
smina_inputs_path.mkdir(exist_ok=True)
smina_outputs_path = data_path / "smina_outputs"
smina_outputs_path.mkdir(exist_ok=True)


# %% [markdown]
# We prepare the pdbqt file for the protein

# %%
if protein_pdbqt_file is None:
    protein_pdbqt_file = smina_inputs_path / "protein.pdbqt"

    prep=Preprocessor()
    prep.prepare_receptor(prepared_protein_pdb_file, protein_pdbqt_file)

# %% [markdown]
# Prepare the bounding box

# %%
ligand = mdtraj.load(ligand_pdb_file)
    
def create_box_from_ligand(ligand):
    xyz=ligand.xyz[0]*10 # convert to Angstrom from nm
    pocket_center = (xyz.max(axis=0) + xyz.min(axis=0)) / 2
    pocket_size = xyz.max(axis=0) - xyz.min(axis=0) + 5
    return Box.from_array(pocket_center, pocket_size)

box=create_box_from_ligand(ligand)
box

# %% [markdown]
# Load molecules from Polaris

# %%
df_mols = pd.read_csv(settings.dataset_file).drop(columns=['UNIQUE_ID'])
df_mols.head()

# %%
df_mols['mols'] = df_mols['smiles'].apply(lambda x: Chem.MolFromSmiles(x))
df_mols.head()

# %%
df_mols['mols'][0]

# %% [markdown]
# Dock them!

# %%
from src.workshop_2_utils import Docking 

docker = Docking(protein_pdbqt_file, box, num_poses=num_poses, exhaustiveness=exhaustiveness) 

if num_mols is None or num_mols > len(df_mols):
    num_mols = len(df_mols)

docker.dock_multiple_mols(
        df_mols["mols"].tolist()[:num_mols],
        input_dir = smina_inputs_path,
        output_dir = smina_outputs_path,
        idxs= list(range(num_mols)),
)


# %% [markdown]
# Read the poses

# %%
poses = dm.read_sdf(smina_outputs_path / "poses.sdf", as_df=True, mol_column="mols", n_jobs=-1)

(smina_outputs_path / "poses.sdf").rename(data_path / "poses.sdf")

# poses.sort_values("minimizedAffinity",inplace=True)

# %% [markdown]
# Need to get rid of duplicates

# %%
if num_poses > 1:
    from rdkit import Chem

    # Function to convert a molecule to its canonical SMILES
    def mol_to_canonical_smiles(mol):
        return Chem.MolToSmiles(Chem.MolFromSmiles(mol), isomericSmiles=True)

    # Apply the function to each molecule in the DataFrame
    poses['canonical_smiles'] = poses['smiles'].apply(mol_to_canonical_smiles)

    # Drop duplicates based on the 'canonical_smiles' column
    poses.drop_duplicates(subset='canonical_smiles', inplace=True)


# %%
poses

# %%
poses.drop(columns=['mols']).to_csv(save_df_file, index=False)

# %%



