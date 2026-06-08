"""Run a single case from the command line.

Usage:
    python -m scripts.run_cli "34yo with sore throat and mild fever for 3 days"
"""
import sys

from mediagent.graph import run_case


def main():
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.run_cli "case description"')
        sys.exit(1)
    text = sys.argv[1]
    state = run_case(patient_input=text)
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(state.get("final_report", "(no report)"))


if __name__ == "__main__":
    main()
