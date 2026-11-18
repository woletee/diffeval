"""Model flags for diffeval run."""


def add_model_flags(parser) -> None:
    parser.add_argument("--backend", default=None)
    parser.add_argument("--pipeline", default=None)
    parser.add_argument("--dtype", default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--guidance", type=float, default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--attention", choices=("sdpa", "xformers", "eager"), default=None)
    parser.add_argument("--variant", default=None)
    parser.add_argument("--batch-size", dest="batch_size", type=int, default=None)
