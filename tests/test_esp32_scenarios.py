"""
ESP32 scenario tests (S6-S10) from Phase 8 integration testing.

These tests validate the complete workflow for ESP32 GPIO configurations:
- Validation (strapping pins, ADC2/WiFi conflicts, flash pins)
- Config generation (sdkconfig-style comments)
- Code generation (arduino, espidf frameworks)
- Syntax verification (brace balance for C/C++)
"""


from helpers import validate_cpp_braces


# ===================================================================
# S6: I2C BME280 + SPI ST7789 display on ESP32 DevKitC (WROOM)
# ===================================================================

class TestS6Esp32I2cSpi:
    """S6: I2C BME280 + SPI ST7789 display on ESP32 DevKitC (WROOM)."""

    def test_validation_passes(self, load_fixture, esp32_platform, helpers):
        """S6 should validate successfully."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_strapping_pin_warnings(self, load_fixture, esp32_platform, helpers):
        """S6 should warn about strapping pins GPIO2 and GPIO5."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "STRAPPING_PIN" in warning_codes

    def test_i2c_pullup_warnings(self, load_fixture, esp32_platform, helpers):
        """S6 should warn about I2C pull-up resistors."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "MISSING_PULLUP" in warning_codes

    def test_arduino_code_generation(self, load_fixture, esp32_platform):
        """S6 Arduino code should have balanced braces."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        result = esp32_platform.generate_code(assignment, "arduino")
        assert result is not None
        assert len(result) > 0
        assert validate_cpp_braces(result)

    def test_espidf_code_generation(self, load_fixture, esp32_platform):
        """S6 ESP-IDF code should have balanced braces."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        result = esp32_platform.generate_code(assignment, "espidf")
        assert result is not None
        assert len(result) > 0
        assert validate_cpp_braces(result)

    def test_arduino_code_contains_expected_patterns(self, load_fixture, esp32_platform):
        """S6 Arduino code should use Wire and SPI."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        code_lower = code.lower()
        assert "wire" in code_lower or "i2c" in code_lower
        assert "spi" in code_lower


# ===================================================================
# S7a: ADC1 with WiFi enabled (valid - ADC1 always works)
# ===================================================================

class TestS7aEsp32Adc1Wifi:
    """S7a: ADC1 with WiFi enabled (valid - ADC1 always works)."""

    def test_validation_passes(self, load_fixture, esp32_platform, helpers):
        """S7a should validate successfully - ADC1 works with WiFi."""
        assignment = load_fixture("s7a_esp32_adc1_wifi.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_no_adc2_wifi_warning(self, load_fixture, esp32_platform, helpers):
        """S7a should NOT produce ADC2_WIFI for ADC1 pin (GPIO34)."""
        assignment = load_fixture("s7a_esp32_adc1_wifi.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        error_codes = helpers.get_error_codes(result)
        assert "ADC2_WIFI" not in warning_codes
        assert "ADC2_WIFI" not in error_codes

    def test_arduino_code_generation(self, load_fixture, esp32_platform):
        """S7a Arduino code should be generated."""
        assignment = load_fixture("s7a_esp32_adc1_wifi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 0


# ===================================================================
# S7b: ADC2 with WiFi enabled (ADC2 conflicts with WiFi)
# ===================================================================

class TestS7bEsp32Adc2Wifi:
    """S7b: ADC2 with WiFi enabled — must detect conflict."""

    def test_adc2_wifi_conflict_detected(self, load_fixture, esp32_platform, helpers):
        """S7b should produce ADC2_WIFI error for GPIO25 with wifi_enabled."""
        assignment = load_fixture("s7b_esp32_adc2_wifi.json")
        result = esp32_platform.validate(assignment)
        # ADC2_WIFI check fires as error because function contains "analog"
        warning_codes = helpers.get_warning_codes(result)
        error_codes = helpers.get_error_codes(result)
        has_adc2_issue = "ADC2_WIFI" in warning_codes or "ADC2_WIFI" in error_codes
        assert has_adc2_issue, "ADC2_WIFI conflict must be detected when wifi_enabled=true"


# ===================================================================
# S8a: Deep sleep wake on RTC GPIO (valid)
# ===================================================================

class TestS8aEsp32RtcGpio:
    """S8a: Deep sleep wake on RTC GPIO (valid)."""

    def test_validation_passes(self, load_fixture, esp32_platform, helpers):
        """S8a should validate successfully - GPIO33 is RTC-capable."""
        assignment = load_fixture("s8a_esp32_rtc_gpio.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_arduino_code_generation(self, load_fixture, esp32_platform):
        """S8a Arduino code should reference INPUT."""
        assignment = load_fixture("s8a_esp32_rtc_gpio.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert "INPUT" in code or "input" in code.lower()

    def test_espidf_code_generation(self, load_fixture, esp32_platform):
        """S8a ESP-IDF code should be generated."""
        assignment = load_fixture("s8a_esp32_rtc_gpio.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        assert code is not None
        assert len(code) > 0


# ===================================================================
# S8b: Non-exposed GPIO (GPIO20 on WROOM - physically unbonded)
# ===================================================================

class TestS8bEsp32NonRtc:
    """S8b: Non-exposed GPIO (GPIO20 on WROOM — should be rejected)."""

    def test_validation_rejects_non_exposed(self, load_fixture, esp32_platform, helpers):
        """S8b should reject GPIO20 — not physically bonded on WROOM module."""
        assignment = load_fixture("s8b_esp32_non_rtc.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_invalid(result)
        error_codes = helpers.get_error_codes(result)
        assert "RESERVED_PIN" in error_codes


# ===================================================================
# S9: SPI LoRa + I2C OLED + UART GPS on ESP32-S3
# ===================================================================

class TestS9Esp32s3Multi:
    """S9: SPI LoRa + I2C OLED + UART GPS on ESP32-S3."""

    def test_validation_passes(self, load_fixture, esp32s3_platform, helpers):
        """S9 should validate on ESP32-S3."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        result = esp32s3_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_gpio6_11_not_flash_pins_on_s3(self, load_fixture, esp32s3_platform, helpers):
        """S9 GPIO9-13 should NOT trigger FLASH_PIN errors on S3."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        result = esp32s3_platform.validate(assignment)
        error_codes = helpers.get_error_codes(result)
        assert "FLASH_PIN" not in error_codes, \
            "GPIO6-11 are NOT flash pins on ESP32-S3"

    def test_i2c_pullup_warnings(self, load_fixture, esp32s3_platform, helpers):
        """S9 should warn about I2C pull-ups."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        result = esp32s3_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "MISSING_PULLUP" in warning_codes

    def test_arduino_code_generation(self, load_fixture, esp32s3_platform):
        """S9 Arduino code should have balanced braces."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        code = esp32s3_platform.generate_code(assignment, "arduino")
        assert validate_cpp_braces(code)

    def test_arduino_code_contains_all_protocols(self, load_fixture, esp32s3_platform):
        """S9 Arduino code should reference SPI, I2C, and UART."""
        assignment = load_fixture("s9_esp32s3_multi.json")
        code = esp32s3_platform.generate_code(assignment, "arduino")
        code_lower = code.lower()
        assert "spi" in code_lower
        assert "wire" in code_lower or "i2c" in code_lower
        assert "serial" in code_lower or "uart" in code_lower


# ===================================================================
# S10: Strapping pins as buttons (GPIO0 + GPIO12)
# ===================================================================

class TestS10Esp32Strapping:
    """S10: Strapping pins as buttons (GPIO0 + GPIO12)."""

    def test_validation_passes(self, load_fixture, esp32_platform, helpers):
        """S10 should validate (strapping pins usable with warnings)."""
        assignment = load_fixture("s10_esp32_strapping.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)

    def test_strapping_pin_warnings_present(self, load_fixture, esp32_platform, helpers):
        """S10 MUST warn about both strapping pins."""
        assignment = load_fixture("s10_esp32_strapping.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "STRAPPING_PIN" in warning_codes
        strapping_count = warning_codes.count("STRAPPING_PIN")
        # GPIO0 gets 1 strapping warning; GPIO12 gets strapping + boot_state = 2
        assert strapping_count >= 2, \
            f"Both GPIO0 and GPIO12 should trigger strapping warnings, got {strapping_count}"

    def test_gpio12_flash_voltage_warning(self, load_fixture, esp32_platform):
        """S10 GPIO12 warning should mention flash voltage risk."""
        assignment = load_fixture("s10_esp32_strapping.json")
        result = esp32_platform.validate(assignment)
        all_messages = " ".join(w.get("message", "") for w in result.warnings)
        all_messages_lower = all_messages.lower()
        has_voltage_warning = (
            "flash voltage" in all_messages_lower or
            "1.8v" in all_messages_lower or
            "mtdi" in all_messages_lower
        )
        assert has_voltage_warning, \
            "GPIO12 warning must mention flash voltage damage risk"

    def test_arduino_code_generation(self, load_fixture, esp32_platform):
        """S10 Arduino code should be generated."""
        assignment = load_fixture("s10_esp32_strapping.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert "INPUT" in code or "input" in code.lower()


# ===================================================================
# Framework Coverage Tests
# ===================================================================

class TestEsp32FrameworkCoverage:
    """Ensure both ESP32 frameworks are exercised."""

    def test_arduino_framework_available(self, load_fixture, esp32_platform):
        """Arduino framework should generate valid code."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert code is not None
        assert len(code) > 100
        assert validate_cpp_braces(code)

    def test_espidf_framework_available(self, load_fixture, esp32_platform):
        """ESP-IDF framework should generate valid code."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        assert code is not None
        assert len(code) > 100
        assert validate_cpp_braces(code)

    def test_arduino_uses_arduino_patterns(self, load_fixture, esp32_platform):
        """Arduino code should use Arduino patterns (pinMode, setup, loop)."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "arduino")
        assert "void setup" in code or "pinMode" in code or "digitalWrite" in code

    def test_espidf_uses_idf_patterns(self, load_fixture, esp32_platform):
        """ESP-IDF code should use IDF patterns (gpio_config, driver/)."""
        assignment = load_fixture("s6_esp32_i2c_spi.json")
        code = esp32_platform.generate_code(assignment, "espidf")
        code_lower = code.lower()
        assert "gpio_config" in code_lower or "driver/" in code or "esp_" in code_lower
