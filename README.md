## Structure

- `data`: data, both raw and preprocessing results
- `notebooks`: notebooks
- `src`: reusable code

## User experience `:)`

Please start by doing stuff in branches, don't commit to main until it's ready to merge.


Create your environment:
```
conda create -n put_here_name_of_your_env
conda activate put_here_name_of_your_env
```

Dependencies might make it hard for us to use a single environment:
make sure to create the environments for your notebooks and either create `requirements.txt`
files or write `!pip install` commands in your notebooks.


## smina environment set-up

```
mamba env create -n smina -f env_smina.yml
conda activate smina
```
