import click
from ec2_metadata import ec2_metadata
from . import ec2
import sys


@click.group()
def main():
    pass


@main.command()
@click.option("-id", "--instance-id", default="")
@click.option("-k", "--tag-key", "--tag-name", "--name", "--key")
@click.option("-v", "--tag-value", "--value", multiple=True)
def has_tag(instance_id, tag_key, tag_value):
    if instance_id == "":
        instance_id = ec2_metadata.instance_id
    instance_ids = ec2.get_instance_ids(tag_key, tag_value)
    if instance_id not in instance_ids:
        sys.exit(1)
