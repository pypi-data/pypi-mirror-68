# The order of the sequence that needs to be implemented:
# Start with a single sls file, just like you started with salt
# Stub out the routines around gathering the initial sls file
# Just use a yaml renderer and get it to where we can manage some basic
# includes to drive to highdata

# Then we can start to fill out renderers while at the same time
# deepening the compiler

# Import python libs
import asyncio
import os
import copy

__func_alias__ = {"compile_": "compile"}


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.idem, recurse=True)
    hub.idem.RUNS = {}
    hub.pop.sub.add("idem.sls")
    hub.pop.sub.add(dyne_name="acct")
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.load_subdirs(hub.exec, recurse=True)
    hub.pop.sub.add(dyne_name="states")
    hub.pop.sub.load_subdirs(hub.states, recurse=True)
    hub.idem.req.init.req_map()


def cli(hub):
    """
    Execute a single idem run from the cli
    """
    hub.pop.config.load(["idem", "acct"], cli="idem")
    hub.pop.loop.start(hub.idem.init.cli_apply())


# If the gathering and cli def funcs grow they should be moved to a plugin
def get_refs(hub):
    """
    Determine where the sls sources are
    """
    sls_sources = []
    slses = []
    for sls in hub.OPT["idem"]["sls"]:
        if os.path.isfile(sls):
            ref = sls.rstrip(".sls")
            slses.append(ref)
            sls_dir = os.path.dirname(sls)
            implied = f"file://{sls_dir}"
            if implied not in sls_sources:
                sls_sources.append(implied)
        else:
            slses.append(sls)
    if hub.OPT["idem"]["tree"]:
        tree = f"file://{hub.OPT['idem']['tree']}"
        if tree not in sls_sources:
            sls_sources.insert(0, tree)
    sls_sources.extend(hub.OPT["idem"]["sls_sources"])
    return {"sls_sources": sls_sources, "sls": slses}


async def cli_apply(hub):
    """
    Run the CLI routine in a loop
    """
    if hub.SUBPARSER == "state":
        await hub.idem.init.cli_sls()
    elif hub.SUBPARSER == "exec":
        await hub.idem.init.cli_exec()


async def cli_sls(hub):
    """
    Execute the cli routine to run states
    """
    src = hub.idem.init.get_refs()
    await hub.idem.init.apply(
        "cli",
        src["sls_sources"],
        hub.OPT["idem"]["render"],
        hub.OPT["idem"]["runtime"],
        ["states"],
        hub.OPT["idem"]["cache_dir"],
        src["sls"],
        hub.OPT["idem"]["test"],
        hub.OPT["acct"]["acct_file"],
        hub.OPT["acct"]["acct_key"],
    )

    errors = hub.idem.RUNS["cli"]["errors"]
    if errors:
        display = getattr(hub, "output.nested.display")(errors)
        print(display)
        return
    running = hub.idem.RUNS["cli"]["running"]
    output = hub.OPT["idem"]["output"]
    display = getattr(hub, f"output.{output}.display")(running)
    print(display)


async def cli_exec(hub):
    exec_path = hub.OPT.idem.exec_func
    exec_args = hub.OPT.idem.exec_args
    args = []
    kwargs = {}
    for arg in exec_args:
        if isinstance(arg, dict):
            kwargs.update(arg)
        else:
            args.append(arg)
    if not exec_path.startswith("exec"):
        exec_path = f"exec.{exec_path}"
    if not hasattr(hub, exec_path):
        print(f"The desired execution is not availabe: {exec_path}")
        return
    ret = getattr(hub, exec_path)(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        ret = await ret
    output = hub.OPT.idem.output
    display = getattr(hub, f"output.{output}.display")(ret)
    print(display)


def create(
    hub, name, sls_sources, render, runtime, subs, cache_dir, test, acct_file, acct_key
):
    """
    Create a new instance to execute against
    """
    hub.idem.RUNS[name] = {
        "sls_sources": sls_sources,
        "render": render,
        "runtime": runtime,
        "subs": subs,
        "cache_dir": cache_dir,
        "states": {},
        "test": test,
        "resolved": set(),
        "files": set(),
        "high": {},
        "post_low": [],
        "errors": [],
        "iorder": 100000,
        "sls_refs": {},
        "blocks": {},
        "running": {},
        "run_num": 1,
        "add_low": [],
    }
    if acct_file and acct_key:
        hub.idem.RUNS[name]["acct"] = hub.acct.init.unlock(acct_file, acct_key)


async def apply(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    subs,
    cache_dir,
    sls,
    test=False,
    acct_file=None,
    acct_key=None,
):
    """
    Run idem!
    """
    hub.idem.init.create(
        name, sls_sources, render, runtime, subs, cache_dir, test, acct_file, acct_key
    )
    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using act/idem
    await hub.idem.resolve.gather(name, *sls)
    if hub.idem.RUNS[name]["errors"]:
        return
    await hub.idem.init.compile(name)
    if hub.idem.RUNS[name]["errors"]:
        return
    ret = await hub.idem.run.init.start(name)


async def compile_(hub, name):
    """
    Compile the data defined in the given run name
    """
    for mod in hub.idem.compiler:
        if hasattr(mod, "stage"):
            ret = mod.stage(name)
            if asyncio.iscoroutine(ret):
                await ret
