"""CLI interface for Modal Boltz."""

import click
import uuid
import os
from modal_boltz import __version__
import modal
from modal.stream_type import StreamType
from .images import boltz_image

@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    """Modal Boltz - A Python CLI tool."""
    ctx.ensure_object(dict)







@main.command()
@click.option('--gpu', required=True, help='GPU type to use for prediction')
@click.option('--input-path', required=True, help='Path to input directory or YAML/FASTA configuration file')
@click.option('--volume-name', required=True, help='Name of the Modal volume to use')
@click.option('--args', default='', help='Additional arguments to pass to the boltz command')
def predict(gpu, input_path, volume_name, args):
    """Run a prediction using Boltz."""
    job_id = str(uuid.uuid4())
    
    # Convert relative path to absolute path
    input_path_abs = os.path.abspath(input_path)
    
    # Check if the input path exists
    if not os.path.exists(input_path_abs):
        click.echo(f"Error: Input path not found: {input_path_abs}", err=True)
        raise click.Abort()
    
    is_directory = os.path.isdir(input_path_abs)
    is_file = os.path.isfile(input_path_abs)
    
    if not (is_directory or is_file):
        click.echo(f"Error: Input path is neither a file nor a directory: {input_path_abs}", err=True)
        raise click.Abort()
    
    # If it's a file, validate it's a YAML or FASTA file
    if is_file and not input_path_abs.lower().endswith(('.yaml', '.yml', '.fasta', '.fa', '.fas')):
        click.echo(f"Error: File must be a YAML file (*.yaml, *.yml) or FASTA file (*.fasta, *.fa, *.fas): {input_path_abs}", err=True)
        raise click.Abort()
    
    click.echo("Running prediction with the following configuration:")
    click.echo(f"Job ID: {job_id}")
    click.echo(f"GPU: {gpu}")
    click.echo(f"Input path: {input_path_abs}")
    click.echo(f"Input type: {'Directory' if is_directory else 'YAML/FASTA file'}")
    click.echo(f"Volume name: {volume_name}")
    if args.strip():
        click.echo(f"Additional args: {args.strip()}")
    
    boltz_volume = modal.Volume.from_name(volume_name, create_if_missing=True)
    
    with boltz_volume.batch_upload() as batch:
        if is_directory:
            # Upload the entire directory
            batch.put_directory(input_path_abs, f"/{job_id}/input")
            input_yaml_path = f"/data/{job_id}/input"
        else:
            # Upload the single file (YAML or FASTA)
            file_extension = os.path.splitext(input_path_abs)[1].lower()
            if file_extension in ['.yaml', '.yml']:
                remote_filename = f"/{job_id}/input.yaml"
            else:  # FASTA files
                remote_filename = f"/{job_id}/input{file_extension}"
            
            batch.put_file(input_path_abs, remote_filename)
            input_yaml_path = f"/data{remote_filename}"
    
    modal_app = modal.App.lookup("boltz_app", create_if_missing=True)

    

    modal_sb = modal.Sandbox.create(
        app=modal_app, 
        volumes={'/data': boltz_volume}, 
        image=boltz_image, 
        gpu=gpu,
    )
    
    try:
        with modal.enable_output():
            # Build the command arguments
            cmd_args = ["boltz", "predict", input_yaml_path, "--out_dir", f"/data/{job_id}/", "--cache", "/data"]
            
            # Add additional arguments if provided
            if args.strip():
                # Split the args string and add to command
                additional_args = args.strip().split()
                cmd_args.extend(additional_args)
            
            sb_handle = modal_sb.exec(
                *cmd_args,
                stdout=StreamType.STDOUT,
                stderr=StreamType.STDOUT,
                timeout=60*60
            )
            sb_handle.wait()
        modal_sb.terminate()
        click.echo(f"Job ID: {job_id}")
    except Exception as e:
        click.echo(f"Error during prediction: {e}", err=True)
        modal_sb.terminate()
        raise click.Abort()


if __name__ == "__main__":
    main()
