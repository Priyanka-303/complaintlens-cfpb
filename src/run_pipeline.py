"""Run the ComplaintLens data pipeline end to end."""

try:
    from .build_marts import build
    from .download_data import download
except ImportError:  # Direct script execution
    from build_marts import build
    from download_data import download


if __name__ == "__main__":
    source = download()
    build(source)
