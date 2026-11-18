"""--strict writes the report and exits 2 when a metric is skipped."""

from diffeval.cli.main import main


def test_strict_geneval(tmp_path):
    out = tmp_path / "out"
    argv = ["run", "--backend", "dummy", "--suite", "core", "--metrics", "geneval", "--output", str(out), "--seeds", "0"]
    assert main(argv) == 0 and (out / "results.json").is_file()
    code = main(argv + ["--strict"])
    written = [out / name for name in ("results.json", "report.md", "report.html")]
    assert code == 2 and all(path.is_file() for path in written)
