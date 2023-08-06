# -*- coding: utf-8 -*-

import click
import subprocess
import tempfile
import time

from spell.api.exceptions import BadRequest
from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
)

from spell.cli.utils.kube_cluster_templates import cluster_statsd_sink_yaml


def echo_delimiter():
    click.echo("---------------------------------------------")


def get_spell_cluster(spell_client, owner, cluster_name):
    """
    Verify valid cluster_name for current owner, and return that cluster
    """
    validate_org_perms(spell_client, owner)
    with api_client_exception_handler():
        if cluster_name is None:
            clusters = spell_client.list_clusters()
            if len(clusters) > 1:
                raise ExitException(
                    "More than one cluster found for owner, please specify a Cluster name"
                )
            return clusters[0]
        return spell_client.get_cluster(
            cluster_name
        )  # This will throw if the cluster name is invalid


def validate_org_perms(spell_client, owner):
    with api_client_exception_handler():
        owner_details = spell_client.get_owner_details()
        if owner_details.type != "organization":
            raise ExitException(
                "Only organizations can create clusters, use `spell owner` "
                "to switch current owner to an organization "
            )
        if owner_details.requestor_role not in ("admin", "manager"):
            raise ExitException(
                "You must be a Manager or Admin with current org {} to proceed".format(owner)
            )


def create_serving_namespace(kconfig, kclient):
    echo_delimiter()
    click.echo("Creating 'serving' namespace...")
    try:
        kconfig.load_kube_config()
        kube_api = kclient.CoreV1Api()
        if len([i for i in kube_api.list_namespace().items if i.metadata.name == "serving"]) > 0:
            click.echo("'serving' namespace already exists!")
        else:
            kube_api.create_namespace(
                kclient.V1Namespace(metadata=kclient.V1ObjectMeta(name="serving"))
            )
            click.echo("'serving' namespace created!")
        subprocess.check_call(
            ("kubectl", "config", "set-context", "--current", "--namespace=serving")
        )
    except Exception as e:
        raise ExitException("ERROR: Creating 'serving' namespace failed. Error was: {}".format(e))


def add_statsd():
    echo_delimiter()
    click.echo("Setting up StatsD...")
    try:
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(cluster_statsd_sink_yaml)
            f.flush()
            subprocess.check_call(
                ("kubectl", "apply", "--namespace", "serving", "--filename", f.name)
            )
        click.echo("StatsD set up!")
    except Exception as e:
        click.echo("ERROR: Setting up StatsD failed. Error was: {}".format(e), err=True)


def block_until_cluster_drained(spell_client, cluster_name):
    """
    Block until cluster is drained. This is necessary because the API will fail to
    drain if we delete the IAM role before the machine types are marked as drained
    """
    num_retries = 10
    for i in range(num_retries):
        try:
            spell_client.is_cluster_drained(cluster_name)
            click.echo("Cluster is drained!")
            return
        except BadRequest:
            # Don't sleep on the last iteration
            if i < num_retries - 1:
                click.echo(
                    "Cluster is still draining all machine types. "
                    "This can take a long time! Retrying in 30s..."
                )
                time.sleep(30)
    raise ExitException(
        "Timed out waiting for Spell to drain the cluster. Please try again "
        "or contact Spell if the problem persists."
    )
