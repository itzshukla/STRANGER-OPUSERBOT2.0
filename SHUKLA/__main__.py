import asyncio
import importlib
from pytgcalls import idle
from . import PLUGINS as plugs
from . import log as logs
from .plugins import ALL_PLUGINS
from . import shukla as run_async_clients
from .modules.clients.enums import run_async_enums
from .modules.helpers.inline import run_async_inline

loop = asyncio.get_event_loop()

async def main():
    # Call the start method of the Shukla instance
    await run_async_clients.start()
    for all_plugin in ALL_PLUGINS:
        imported_plugin = importlib.import_module(
            "SHUKLA.plugins" + all_plugin
        )
        if (hasattr
            (
                imported_plugin, "__NAME__"
            ) and imported_plugin.__NAME__
        ):
            imported_plugin.__NAME__ = imported_plugin.__NAME__
            if (
                hasattr(
                    imported_plugin, "__MENU__"
                ) and imported_plugin.__MENU__
            ):
                plugs[imported_plugin.__NAME__.lower()
                ] = imported_plugin
    await run_async_enums()
    logs.info(">> Successfully Imported All Plugins.")
    await run_async_inline()
    logs.info("Successfully Deployed !!")
    logs.info("Do Visit - @MASTIWITHFRIENDSXD")
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Userbot Stopped !\nGoodBye ...")