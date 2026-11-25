import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from assembler import translate_to_ir, ir_to_bytes

class TestAssembler(unittest.TestCase):
    def test_translation(self):
        commands = [
            {"name": "load_const", "b": 163, "c": 2},
            {"name": "read", "b": 14, "c": 40},
            {"name": "write", "b": 49, "c": 168},
            {"name": "sqrt", "b": 20, "c": 74}
        ]
        ir = translate_to_ir(commands)
        
        self.assertEqual(list(ir_to_bytes(ir[0])), [0x3E, 0x0A, 0x00, 0x08, 0x00])
        self.assertEqual(list(ir_to_bytes(ir[1])), [0xE0, 0x40, 0x01])
        self.assertEqual(list(ir_to_bytes(ir[2])), [0x14, 0x43, 0x05, 0x00, 0x00])
        self.assertEqual(list(ir_to_bytes(ir[3])), [0x49, 0x51, 0x02])

if __name__ == "__main__":
    unittest.main()