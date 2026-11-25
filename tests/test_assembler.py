"""Unit tests for assembler."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from assembler import translate_to_ir, ir_to_bytes


class TestAssembler(unittest.TestCase):
    """Tests for UVM assembler."""

    def test_translation(self):
        """Test all commands from specification."""
        commands = [
            {"name": "load_const", "b": 163, "c": 2},
            {"name": "read", "b": 14, "c": 40},
            {"name": "write", "b": 49, "c": 168},
            {"name": "sqrt", "b": 20, "c": 74}
        ]
        ir = translate_to_ir(commands)

        res_0 = list(ir_to_bytes(ir[0]))
        exp_0 = [0x3E, 0x0A, 0x00, 0x08, 0x00]
        self.assertEqual(res_0, exp_0)

        res_1 = list(ir_to_bytes(ir[1]))
        exp_1 = [0xE0, 0x40, 0x01]
        self.assertEqual(res_1, exp_1)

        res_2 = list(ir_to_bytes(ir[2]))
        exp_2 = [0x14, 0x43, 0x05, 0x00, 0x00]
        self.assertEqual(res_2, exp_2)

        res_3 = list(ir_to_bytes(ir[3]))
        exp_3 = [0x49, 0x51, 0x02]
        self.assertEqual(res_3, exp_3)


if __name__ == "__main__":
    unittest.main()