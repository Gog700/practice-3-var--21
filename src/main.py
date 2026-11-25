"""Main entry point for UVM assembler."""

import argparse
import sys

from assembler import parse_yaml, translate_to_ir, ir_to_bytes


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="UVM Assembler")
    parser.add_argument(
        "--input",
        required=True,
        help="Путь к файлу .yaml"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Путь к бинарному файлу"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Режим тестирования"
    )
    return parser.parse_args()


def main() -> None:
    """Run the assembler."""
    args = parse_args()

    try:
        commands = parse_yaml(args.input)
        ir = translate_to_ir(commands)
    except Exception as exc:
        print(f"Ошибка ассемблирования: {exc}")
        sys.exit(1)

    binary_data = bytearray()

    for cmd in ir:
        b_bytes = ir_to_bytes(cmd)
        binary_data.extend(b_bytes)

        if args.test:
            hex_str = ", ".join(f"0x{b:02X}" for b in b_bytes)
            test_msg = f"Тест (A={cmd['A']}, B={cmd['B']}, C={cmd['C']}):"
            print(test_msg)
            print(hex_str)

    with open(args.output, "wb") as f:
        f.write(binary_data)

    if not args.test:
        size = len(binary_data)
        print(f"Размер файла: {size} байт")


if __name__ == "__main__":
    main()