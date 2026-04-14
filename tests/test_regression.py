"""
Regression tests from Phase 8 integration testing.

These tests verify that core functionality remains working after any changes.
ESP32-only — RPi regression tests were removed during ESP32 specialization.
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from platforms import get_platform


# ===================================================================
# Check A: Basic ESP32 validation works
# ===================================================================

class TestBasicValidation:
    """Regression check: Basic ESP32 validation works."""

    def test_esp32_basic_validation(self, load_fixture, esp32_platform, helpers):
        """Check E: Basic ESP32 GPIO output validates."""
        assignment = load_fixture("regression_esp32_basic.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_valid(result)


# ===================================================================
# Check B: Invalid platforms are rejected
# ===================================================================

class TestInvalidPlatformRejection:
    """Regression check B: Invalid platforms are rejected."""

    def test_invalid_platform_rejected(self):
        """Check B: Invalid platform string should raise ValueError."""
        with pytest.raises(ValueError):
            get_platform("fooboard")


# ===================================================================
# Check C: Framework-platform mismatches rejected
# ===================================================================

class TestFrameworkMismatch:
    """Regression check: Framework-platform mismatches rejected."""

    def test_gpiozero_rejected_for_esp32(self, load_fixture, esp32_platform):
        """gpiozero framework should be rejected for ESP32."""
        assignment = load_fixture("regression_esp32_basic.json")
        with pytest.raises(ValueError):
            esp32_platform.generate_code(assignment, "gpiozero")


# ===================================================================
# Check F: ADC2/WiFi conflict detection
# ===================================================================

class TestAdc2WifiConflict:
    """Regression check F: ADC2/WiFi conflict detection."""

    def test_adc2_wifi_conflict_detected(self, load_fixture, esp32_platform, helpers):
        """Check F: ADC2 pin with wifi_enabled should produce ADC2_WIFI."""
        assignment = load_fixture("s7b_esp32_adc2_wifi.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        error_codes = helpers.get_error_codes(result)
        assert "ADC2_WIFI" in warning_codes or "ADC2_WIFI" in error_codes


# ===================================================================
# Checks G, H: Flash pin handling
# ===================================================================

class TestFlashPinProtection:
    """Regression checks G, H: Flash pin handling."""

    def test_base_esp32_flash_pin_blocked(self, load_fixture, esp32_platform, helpers):
        """Check G: GPIO6 should be rejected on base ESP32."""
        assignment = load_fixture("regression_esp32_flash_pin.json")
        result = esp32_platform.validate(assignment)
        helpers.assert_invalid(result)
        error_codes = helpers.get_error_codes(result)
        assert "FLASH_PIN" in error_codes

    def test_esp32s3_flash_pin_allowed(self, load_fixture, esp32s3_platform, helpers):
        """Check H: GPIO6 should be allowed on ESP32-S3."""
        assignment = load_fixture("regression_esp32s3_flash_pin.json")
        result = esp32s3_platform.validate(assignment)
        helpers.assert_valid(result)
        error_codes = helpers.get_error_codes(result)
        assert "FLASH_PIN" not in error_codes


# ===================================================================
# Bug fix: Strapping pins are variant-aware
# ===================================================================

class TestStrappingPinVariantAwareness:
    """Bug fix verification: Strapping pins are variant-aware."""

    def test_base_esp32_strapping_pins(self, load_fixture, esp32_platform, helpers):
        """Base ESP32 should warn for GPIO0, 2, 5, 12, 15."""
        assignment = load_fixture("s10_esp32_strapping.json")
        result = esp32_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "STRAPPING_PIN" in warning_codes

    def test_esp32s3_strapping_pins(self, load_fixture, esp32s3_platform, helpers):
        """ESP32-S3 should warn for GPIO0, 3, 45, 46 (different set)."""
        assignment = load_fixture("regression_esp32s3_strapping.json")
        result = esp32s3_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "STRAPPING_PIN" in warning_codes
        strapping_count = warning_codes.count("STRAPPING_PIN")
        assert strapping_count >= 3, \
            f"All three S3 strapping pins should trigger warnings, got {strapping_count}"

    def test_gpio5_not_strapping_on_s3(self, esp32s3_platform, helpers):
        """GPIO5 should NOT be a strapping pin on ESP32-S3."""
        assignment = {
            "platform": "esp32s3",
            "variant": "esp32s3",
            "module": "WROOM",
            "wifi_enabled": False,
            "pins": [
                {"gpio": 5, "function": "OUTPUT", "protocol_bus": "gpio",
                 "device": "LED", "direction": "output", "pull": "none",
                 "speed_hz": 0, "notes": ""}
            ]
        }
        result = esp32s3_platform.validate(assignment)
        warning_codes = helpers.get_warning_codes(result)
        assert "STRAPPING_PIN" not in warning_codes
        helpers.assert_valid(result)
