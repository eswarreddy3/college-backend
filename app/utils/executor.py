"""
Code execution engine using local subprocesses.
Supports: Python, JavaScript (Node.js), Java (if javac available), C++ (if g++ available)
"""
import subprocess
import tempfile
import os
import sys
import time
import shutil

TIMEOUT_SECONDS = 5
MAX_OUTPUT_LEN = 4096  # chars

# Language configs: (file_suffix, build_cmd_fn, run_cmd_fn)
# build_cmd_fn(tmpdir, src_file) -> list[str] or None
# run_cmd_fn(tmpdir, src_file) -> list[str]

PYTHON_BIN = sys.executable  # Use the same venv python


def _python_run(tmpdir, src):
    return [PYTHON_BIN, src]


def _node_run(tmpdir, src):
    node = shutil.which("node") or "node"
    return [node, src]


def _java_build(tmpdir, src):
    javac = shutil.which("javac")
    if not javac:
        return None
    return [javac, src]


def _java_run(tmpdir, src):
    java = shutil.which("java") or "java"
    return [java, "-cp", tmpdir, "Solution"]


def _cpp_build(tmpdir, src):
    gpp = shutil.which("g++")
    if not gpp:
        return None
    out = os.path.join(tmpdir, "solution.exe" if os.name == "nt" else "solution")
    return [gpp, src, "-o", out, "-O2", "-std=c++17"]


def _cpp_run(tmpdir, src):
    out = os.path.join(tmpdir, "solution.exe" if os.name == "nt" else "solution")
    return [out]


LANG_CONFIG = {
    "python": {
        "suffix": ".py",
        "build": None,
        "run": _python_run,
    },
    "javascript": {
        "suffix": ".js",
        "build": None,
        "run": _node_run,
    },
    "java": {
        "suffix": ".java",
        "filename": "Solution.java",  # Java requires class name = filename
        "build": _java_build,
        "run": _java_run,
    },
    "cpp": {
        "suffix": ".cpp",
        "build": _cpp_build,
        "run": _cpp_run,
    },
}


class ExecutionResult:
    def __init__(self, stdout="", stderr="", runtime_ms=0, error=None):
        self.stdout = stdout.strip()
        self.stderr = stderr.strip()[:MAX_OUTPUT_LEN]
        self.runtime_ms = runtime_ms
        self.error = error  # "timeout" | "compile_error" | "runtime_error" | None

    @property
    def success(self):
        return self.error is None

    def to_dict(self):
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "runtime_ms": self.runtime_ms,
            "error": self.error,
        }


def execute(language: str, code: str, stdin: str = "") -> ExecutionResult:
    """Execute code in the given language with the given stdin. Returns ExecutionResult."""
    lang = language.lower()
    if lang not in LANG_CONFIG:
        return ExecutionResult(error=f"Unsupported language: {language}")

    config = LANG_CONFIG[lang]

    # Check runtime availability
    if lang == "javascript" and not shutil.which("node"):
        return ExecutionResult(error="Node.js not found on server")
    if lang == "java" and not shutil.which("javac"):
        return ExecutionResult(error="Java compiler not found on server")
    if lang == "cpp" and not shutil.which("g++"):
        return ExecutionResult(error="C++ compiler (g++) not found on server")

    tmpdir = tempfile.mkdtemp()
    try:
        # Write source file
        filename = config.get("filename") or (f"solution{config['suffix']}")
        src_path = os.path.join(tmpdir, filename)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(code)

        # Compile if needed
        if config["build"]:
            build_cmd = config["build"](tmpdir, src_path)
            if build_cmd is None:
                return ExecutionResult(error=f"Compiler not available for {language}")
            try:
                comp = subprocess.run(
                    build_cmd,
                    capture_output=True, text=True, timeout=30
                )
                if comp.returncode != 0:
                    return ExecutionResult(
                        stderr=comp.stderr or comp.stdout,
                        error="compile_error"
                    )
            except subprocess.TimeoutExpired:
                return ExecutionResult(error="compile_error")

        # Run
        run_cmd = config["run"](tmpdir, src_path)
        start = time.time()
        try:
            proc = subprocess.run(
                run_cmd,
                input=stdin,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=tmpdir,
            )
            elapsed = int((time.time() - start) * 1000)

            if proc.returncode != 0:
                return ExecutionResult(
                    stdout=proc.stdout[:MAX_OUTPUT_LEN],
                    stderr=proc.stderr[:MAX_OUTPUT_LEN],
                    runtime_ms=elapsed,
                    error="runtime_error",
                )
            return ExecutionResult(
                stdout=proc.stdout[:MAX_OUTPUT_LEN],
                stderr=proc.stderr[:MAX_OUTPUT_LEN],
                runtime_ms=elapsed,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(error="timeout", runtime_ms=TIMEOUT_SECONDS * 1000)

    finally:
        # Cleanup temp dir
        try:
            import shutil as sh
            sh.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass


def run_test_cases(language: str, code: str, test_cases: list) -> list:
    """
    Run code against multiple test cases.
    Each test case: {"input": str, "expected": str}
    Returns list of result dicts.
    """
    results = []
    for i, tc in enumerate(test_cases):
        stdin = tc.get("input", "")
        expected = tc.get("expected", "").strip()
        result = execute(language, code, stdin)

        actual = result.stdout.strip() if result.success else ""

        passed = result.success and (actual == expected)

        results.append({
            "id": i + 1,
            "input": stdin,
            "expected": expected,
            "got": actual if result.success else f"[{result.error}] {result.stderr[:200]}",
            "passed": passed,
            "runtime_ms": result.runtime_ms,
            "error": result.error,
        })

    return results
