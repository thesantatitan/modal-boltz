# Modal Boltz

A Python CLI tool for running Boltz protein structure predictions on Modal cloud infrastructure.

## Prerequisites

Before using this tool, you need:

1. **Modal Account**: Sign up at [modal.com](https://modal.com) and get your API token
2. **Modal CLI**: Install and authenticate with Modal:

   ```bash
   pip install modal
   modal token set
   ```

## Installation


```bash
pip install git+https://github.com/thesantatitan/modal-boltz.git
```

### Using uv (recommended for development)

```bash
uv tool install git+https://github.com/thesantatitan/modal-boltz.git
```

## Usage

The CLI provides a `predict` command to run Boltz protein structure predictions on Modal:

```bash
modal-boltz predict --gpu <gpu_type> --input-path <path> --volume-name <volume>
```

### Required Parameters

- `--gpu`: GPU type to use (e.g., `A10G`, `A100`, `H100`)
- `--input-path`: Path to input YAML configuration file, FASTA file, or directory
- `--volume-name`: Name of the Modal volume for data storage

### Optional Parameters

- `--args`: Additional arguments to pass to the Boltz command

### Examples

```bash
# Run prediction with a YAML configuration file
modal-boltz predict --gpu A10G --input-path example.yaml --volume-name my-boltz-data

# Run prediction with a FASTA file
modal-boltz predict --gpu A100 --input-path protein.fasta --volume-name my-boltz-data

# Run prediction with additional Boltz arguments
modal-boltz predict --gpu H100 --input-path config.yaml --volume-name my-data --args "--num_samples 5 --recycling 3"

# Show help
modal-boltz --help
modal-boltz predict --help
```

## Boltz

For more information on how to use Boltz, refer to the [Boltz documentation](https://github.com/jwohlwend/boltz/tree/main).