# Import python libs
import asyncio


async def modify(hub, name, chunk):
    """
    Check the state containing the target func and call the mod_creds
    function if present. Therefore gathering the list of creds systems
    to use
    """
    state = chunk["state"].split(".")[0]
    subs = []
    if hasattr(hub, f"states.{state}.ACCT"):
        subs = getattr(hub, f"states.{state}.ACCT")
    elif hasattr(hub, f"{state}.ACCT"):
        subs = getattr(hub, f"{state}.ACCT")
    profile = chunk.pop("acct_profile", "default")
    chunk["ctx"]["acct"] = await hub.acct.init.gather(subs, profile)
    return chunk
