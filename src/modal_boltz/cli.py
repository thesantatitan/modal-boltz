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
@click.option('--name', default='World', help='Name to greet')
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello {name} from modal-boltz!")


@main.command()
def info():
    """Show information about modal-boltz."""
    click.echo(f"Modal Boltz v{__version__}")
    click.echo("A Python CLI tool built with Modal and Boltz")




@main.command()
@click.option('--gpu', required=True, help='GPU type to use for prediction')
@click.option('--yaml-file', required=True, help='Path to YAML configuration file')
@click.option('--volume-name', required=True, help='Name of the Modal volume to use')
def predict(gpu, yaml_file, volume_name):
    """Run a prediction using Boltz."""
    job_id = str(uuid.uuid4())
    
    # Convert relative path to absolute path
    yaml_file_path = os.path.abspath(yaml_file)
    
    # Check if the YAML file exists
    if not os.path.exists(yaml_file_path):
        click.echo(f"Error: YAML file not found at path: {yaml_file_path}", err=True)
        raise click.Abort()
    
    if not os.path.isfile(yaml_file_path):
        click.echo(f"Error: Path exists but is not a file: {yaml_file_path}", err=True)
        raise click.Abort()
    
    click.echo("Running prediction with the following configuration:")
    click.echo(f"Job ID: {job_id}")
    click.echo(f"GPU: {gpu}")
    click.echo(f"YAML file: {yaml_file_path}")
    click.echo(f"Volume name: {volume_name}")
    
    boltz_volume = modal.Volume.from_name(volume_name, create_if_missing=True)
    
    with boltz_volume.batch_upload() as batch:
        batch.put_file(yaml_file_path, f"/{job_id}/input.yaml")
    
    modal_app = modal.App.lookup("boltz_app", create_if_missing=True)

    

    modal_sb = modal.Sandbox.create(
        app=modal_app, 
        volumes={'/data': boltz_volume}, 
        image=boltz_image, 
        gpu=gpu,
    )
    
    with modal.enable_output():
        sb_handle = modal_sb.exec(
            "boltz", "predict", f"/data/{job_id}/input.yaml", "--out_dir", f"/data/{job_id}/", "--cache", "/data", "--use_msa_server",
            stdout=StreamType.STDOUT,
            stderr=StreamType.STDOUT,
            timeout=60*60
        )
        sb_handle.wait()
    modal_sb.terminate()
    click.echo(f"Job ID: {job_id}")
    


if __name__ == "__main__":
    main()
