import click
from .generator import generate_outputs

@click.command()
@click.argument('idea')
@click.option('--output', type=click.Path(), help='File to save the output')
def run_cli(idea, output):
    """Run the DreamForge CLI with a startup idea."""
    outputs = generate_outputs(idea)
    if output:
        with open(output, 'w') as f:
            f.write(outputs)
    else:
        print(outputs)

if __name__ == "__main__":
    run_cli()