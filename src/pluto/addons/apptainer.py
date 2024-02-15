#!/usr/bin/env python3
"""This module contains the apptainer addon provisioning method."""
import asyncio

from pluto.drivers import Cluster


async def provision_apptainer(cluster: Cluster) -> None:
    """Add the apptainer service to the deployment."""
    await asyncio.gather(
        cluster.deploy(
            "apptainer",
            channel="edge",
            num_units=0,
            base="ubuntu@22.04",
        ),
    )
    await asyncio.gather(cluster.integrate("slurmd:juju-info", "apptainer:juju-info"))

    async with cluster.quick_fire():
        await cluster.wait(apps=["apptainer"], status="active", raise_on_error=False, timeout=1200)
