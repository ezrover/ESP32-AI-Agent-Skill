"""
Cross-platform scenario tests (S11) — ESP32 side only.

This skill is ESP32-only. RPi tests were removed during ESP32 specialization.
Tests verify ESP32 config and code generation produce correct, uncontaminated output.
"""


from helpers import validate_cpp_braces


# ===================================================================
# S11b: BME280 + SD Card on ESP32
# ===================================================================

class TestS11bCrossPlatformEsp32:
    """S11b: BME280 + SD Card on ESP32."""

    def test_validation_passes(self, load_fixture, esp32_platform, helpers):
        """S11b ESP32 should validate successfully."""
        assignment = load_fixture("s11b_esp32_bmesd.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_config_has_esp32_format(self, load_fixture, esp32_platform):
        """S11b ESP32 config should NOT use dtparam format."""
        assignment = load_fixture("s11b_esp32_bmesd.json")
        result = esp32_platform.generate_config(assignment)
        config_text = " ".join(result.config_lines)
        assert "dtparam" not in config_text
        assert "dtoverlay" not in config_text

    def test_code_is_cpp(self, load_fixture, esp32_platform):
        """S11b ESP32 code should be valid C++ (balanced braces)."""
        assignment = load_fixture("s11b_esp32_bmesd.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert validate_cpp_braces(code)

    def test_no_rpi_contamination(self, load_fixture, esp32_platform):
        """S11b ESP32 code should NOT contain RPi patterns."""
        assignment = load_fixture("s11b_esp32_bmesd.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        code_lower = code.lower()
        assert "gpiozero" not in code_lower
        assert "rpi.gpio" not in code_lower
        assert "pigpio" not in code_lower
        assert "dtparam" not in code_lower
