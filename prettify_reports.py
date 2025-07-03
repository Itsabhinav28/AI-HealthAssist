def prettify_report(input_path, output_path=None):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove lines with 'none' or 'no data' (case-insensitive)
    filtered = [
        line for line in lines
        if "none" not in line.lower() and "no data" not in line.lower()
    ]

    # Prettify: Add spacing, bold section headers, and bullet points
    pretty_lines = []
    for line in filtered:
        stripped = line.strip()
        if not stripped:
            pretty_lines.append("")
            continue
        # Section headers (lines ending with ':')
        if stripped.endswith(":"):
            pretty_lines.append(f"\n\033[1m{stripped}\033[0m")  # Bold in terminal
        # Bullet points
        elif stripped.startswith("*") or stripped.startswith("-"):
            pretty_lines.append(f"  • {stripped.lstrip('*- ')}")
        else:
            pretty_lines.append(stripped)

    pretty_report = "\n".join(pretty_lines)

    # Optionally save to a new file
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_report)
    return pretty_report

# Example usage:
if __name__ == "__main__":
    # Change the file path as needed
    result = prettify_report("Results/final_diagnosis.txt", "Results/final_diagnosis_pretty.txt")
    print(result)