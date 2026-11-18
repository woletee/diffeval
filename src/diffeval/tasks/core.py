"""Register the bundled core suite."""

from diffeval.registry.register import register
from diffeval.registry.tables import TASKS
from diffeval.tasks.load_bundled import load_bundled


class Core:
    description = "Four synthetic prompts for a CPU smoke run."

    def load(self):
        return load_bundled("core.yaml")


register(TASKS, "core")(Core())
