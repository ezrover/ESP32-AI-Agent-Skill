"""
Syntax validation tests for ESP32 frameworks.

Ensures generated code is syntactically valid:
- C/C++ (Arduino, ESP-IDF): Balanced braces
"""


from helpers import validate_cpp_braces


# ===================================================================
# Arduino framework
# ===================================================================

class TestArduinoSyntax:
    """Arduino framework syntax validation."""

    def test_arduino_syntax_s6(self, load_fixture, esp32_platform):
        """s6 I2C+SPI fixture generates valid Arduino C++."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s6_esp32_i2c_spi.json"

    def test_arduino_syntax_s7a(self, load_fixture, esp32_platform):
        """s7a ADC1+WiFi fixture generates valid Arduino C++."""
        assignment = load_fixture("s7a_esp32_adc1_wifi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s7a_esp32_adc1_wifi.json"

    def test_arduino_syntax_s8a(self, load_fixture, esp32_platform):
        """s8a RTC GPIO fixture generates valid Arduino C++."""
        assignment = load_fixture("s8a_esp32_rtc_gpio.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s8a_esp32_rtc_gpio.json"

    def test_arduino_syntax_s10(self, load_fixture, esp32_platform):
        """s10 strapping pin fixture generates valid Arduino C++."""
        assignment = load_fixture("s10_esp32_strapping.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s10_esp32_strapping.json"

    def test_arduino_syntax_s11b(self, load_fixture, esp32_platform):
        """s11b BME+SD fixture generates valid Arduino C++."""
        assignment = load_fixture("s11b_esp32_bmesd.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s11b_esp32_bmesd.json"

    def test_arduino_syntax_valid_esp32s3(self, load_fixture, esp32s3_platform):
        """ESP32-S3 multi fixture should generate valid Arduino C++."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        code = esp32s3_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s9_esp32s3_multi.json"


# ===================================================================
# ESP-IDF framework
# ===================================================================

class TestEspidfSyntax:
    """ESP-IDF framework syntax validation."""

    def test_espidf_syntax_s6(self, load_fixture, esp32_platform):
        """s6 I2C+SPI fixture generates valid ESP-IDF C."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s6_esp32_i2c_spi.json"

    def test_espidf_syntax_s8a(self, load_fixture, esp32_platform):
        """s8a RTC GPIO fixture generates valid ESP-IDF C."""
        assignment = load_fixture("s8a_esp32_rtc_gpio.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        assert code is not None
        assert len(code) > 0
        assert validate_cpp_braces(code), "Unbalanced braces in s8a_esp32_rtc_gpio.json"


# ===================================================================
# Meta: both ESP32 frameworks covered
# ===================================================================

class TestAllFrameworksCovered:
    """Meta-test to ensure both ESP32 frameworks have been exercised."""

    def test_arduino_tested(self, load_fixture, esp32_platform):
        """arduino framework is available and tested."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert "void" in code or "setup" in code.lower()

    def test_espidf_tested(self, load_fixture, esp32_platform):
        """espidf framework is available and tested."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        assert "gpio" in code.lower() or "esp" in code.lower()
