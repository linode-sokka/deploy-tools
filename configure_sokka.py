#!/usr/bin/env python3
import subprocess
from typing import IO
from typing import Optional
from urllib.parse import urljoin

import click
import requests


def git_sha(directory: str = ".") -> str:
    """Return the git sha for this repo"""
    cmd = f"git -C {directory} rev-parse --verify HEAD"
    return subprocess.check_output(cmd, shell=True, text=True).strip()


@click.command()
@click.option(
    "--host",
    type=str,
    default="http://deploy.alexrudy.local/",  # TODO: Figure out a sensible default, or maybe remove
    envvar="DEPLOYER_HOST",
    help="Host for deployer",
)
@click.option(
    "--api-endpoint", type=str, default="/compose/projects/", envvar="DEPLOYER_API_ENDPOINT", help="Path to endpoint"
)
@click.option(
    "-P", "--project", type=str, envvar="COMPOSE_PROJECT_NAME", required=True, help="Project name in deployer"
)
@click.option("--token", type=str, envvar="DEPLOYER_TOKEN", required=True, help="API Token for deployer")
@click.option("--version", type=str, help="Version information for this configuration")
@click.argument("configuration", type=click.File("rb"))
def main(
    host: str, api_endpoint: str, project: str, version: Optional[str], token: str, configuration: IO[bytes]
) -> None:
    """Send a docker configuration to deployer.

    docker-compose config | configure-sokka -P my-project -
    """

    if version is None:
        version = git_sha()

    headers = {"Authorization": f"Bearer: {token}"}
    url = urljoin(host, f"{api_endpoint}{project}/configure/{version}/")

    click.echo(f"POST {url}", err=True)

    result = requests.post(url, data=configuration.read(), allow_redirects=False, headers=headers)
    if result.status_code >= 400:
        msg = click.style("[ERROR]", fg="red")
        click.echo(f"{msg} {result.status_code} Error in HTTP response:", err=True)
        click.echo(result.text, err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
