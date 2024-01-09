"""
The module `spacial_pokemon_pvp` implements a Pokemon and space based `PackageVersionProvider`.
"""
import asyncio
from functools import lru_cache
from typing import Tuple

import aiohttp

from pylibtemplate.config.paths.path import RemotePath
from pylibtemplate.config.versioning.version import Version
from pylibtemplate.config.packaging import git
from pylibtemplate.config.packaging.package_version import PackageVersion
from pylibtemplate.config.packaging.package_version_providers.package_version_provider import (
    PackageVersionProvider,
)

__pdoc__ = {"PokemonAPI": False}


class PokemonAPI:
    """
    Implementation of Pokemon API source.
    """

    url: RemotePath = RemotePath("https", "pokeapi.co", "/api/v2/pokemon/")

    _pokemon_image_base = RemotePath(
        "https",
        "raw.githubusercontent.com",
        "/PokeAPI/sprites/master/sprites/pokemon/versions/",
    )

    async def auth(self):
        pass

    async def read(self, number: int):
        """
        Get the pokemon name, generation sprite and default sprite from PokeAPI.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url / str(number)) as response:
                pokemon = await response.json()

        default_img = pokemon.get("sprites").get("front_default")
        generation_path = None

        if number <= 151:
            generation_path = "generation-i/yellow/"
        elif 151 < number <= 251:
            generation_path = "generation-ii/crystal/"
        elif 251 < number <= 386:
            generation_path = "generation-iii/emerald/"
        elif 386 < number <= 493:
            generation_path = "generation-iv/platinum/"
        elif 493 < number <= 721:
            generation_path = "generation-vi/x-y/"
        elif 721 < number <= 807:
            generation_path = "generation-vii/ultra-sun-ultra-moon/"
        elif 807 < number <= 898:
            generation_path = "generation-viii/icons/"

        return (
            pokemon.get("name").capitalize(),
            PokemonAPI._pokemon_image_base / generation_path / f"{number}.png"
            if generation_path
            else default_img,
            default_img,
        )


class SPokemonPVProvider(PackageVersionProvider):
    """
    Spacial Pokemon Package Version Provider.

    This version provider generates a custom description for every `Version` object, composed
    by Pokemon names (minor versions), Planets (medium versions) and Stars Systems (major versions).
    The major version is not used to compose the description, it's only used to provide Planets for
    medium versions. The number reference starts in 0.

    > And yes, for us Pluto is a planet!!!!!!!

    Example:

        - Version(1,0,0) -> "Mercurial Bulbasaur" # First Planet on solar system and first pokemon.
        - Version(1,2,3) -> "Terrestrial Charmander" # Third Planet on solar system and 4th pokemon.
    """

    _planets = [
        (
            "Mercurial",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Mercury-icon.png",
        ),
        (
            "Venusian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Venus-icon.png",
        ),
        (
            "Terrestial",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Earth-icon.png",
        ),
        (
            "Martian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Mars-icon.png",
        ),
        (
            "Jupiterian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Jupiter-icon.png",
        ),
        (
            "Saturnian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Saturn-icon.png",
        ),
        (
            "Uranian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Uranus-icon.png",
        ),
        (
            "Neptunian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Neptune-icon.png",
        ),
        (
            "Plutonian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Pluto-icon.png",
        ),
        (
            "X Planetarian",
            "https://icons.iconarchive.com/icons/dan-wiersma/solar-system/128/Orb-icon.png",
        ),
    ]

    @staticmethod
    def _get_planet(number: int) -> Tuple[str, str]:
        """
        Get the correspondent Planet. In case of `number > 9` the last planet will be provided.
        """
        return (
            SPokemonPVProvider._planets[number]
            if number < len(SPokemonPVProvider._planets)
            else SPokemonPVProvider._planets[-1]
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def provide(version: Version) -> PackageVersion:
        """
        Provide the PackageVersion object with Space Pokemon description and labels with
        url images.

        `labels`: Dict(
            planet_url={planet image url},
            pokemon_url={Pokemon image URL},
            default_pokemon_url={Pokemon default image}
            )
        """
        pname, pimage, dpimage = asyncio.run(PokemonAPI().read(version.minor + 1))
        plname, plimage = SPokemonPVProvider._get_planet(version.medium)
        return PackageVersion(
            version.major,
            version.medium,
            version.minor,
            git.repo.active_branch.name,
            f"{plname} {pname}",
            dict(planet_url=plimage, pokemon_url=pimage, default_pokemon_url=dpimage),
        )
