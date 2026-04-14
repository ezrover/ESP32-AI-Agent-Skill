# ESP32

A Claude Code plugin for ESP32 embedded systems development. Provides expert-level chip selection, GPIO pin validation with anti-bricking safety checks, code generation for Arduino and ESP-IDF, and comprehensive reference documentation for LVGL and Waveshare hardware.

## Installation

```bash
claude /install-plugin https://github.com/ezrover/ESP32-AI-Agent-Skill
```

Or install from a local clone:

```bash
git clone https://github.com/ezrover/ESP32-AI-Agent-Skill.git
claude /install-plugin ./ESP32-AI-Agent-Skill
```

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.9+ (for validation and code generation scripts)

## Overview

Once installed, Claude automatically activates this plugin when you work on ESP32 projects. It loads hardware reference data on demand and uses validation scripts to prevent common mistakes that can damage hardware.

**What it covers:**

- **Chip selection** across 9 ESP32 variants (ESP32, S2, S3, C3, C6, C2, C5, H2, P4)
- **GPIO validation** that catches strapping pin traps, ADC2/Wi-Fi conflicts, flash pin violations, and input-only pin misuse
- **Code generation** for Arduino (`setup()`/`loop()`) and ESP-IDF (`app_main()`) with correct bus initialization
- **LVGL references** for versions 8.2 through 9.5 with API docs, widget catalogs, and migration guides
- **Waveshare board references** for 60+ dev boards and LCD displays with full pinout tables

## Usage

Ask Claude naturally about any ESP32 topic:

```
I need to wire a BME280 sensor and ST7789 display to an ESP32-S3 with WiFi
```

```
Generate ESP-IDF initialization code for my pin assignments on ESP32-C6
```

```
What changed between LVGL v8 and v9? Which version should I use with ESP32-S3?
```

```
Show me the pinout for the Waveshare ESP32-S3 Touch LCD 4.3 inch board
```

Claude will load the relevant reference files, validate your configuration, and generate working code.

### Validation Scripts

The plugin includes Python scripts that Claude invokes during its workflow. You can also run them directly:

```bash
# Validate a GPIO pin assignment
echo '{"platform":"esp32s3","pins":[{"gpio":21,"function":"I2C_SDA","protocol_bus":"i2c"}]}' \
  | python scripts/validate_pinmap.py

# Generate Arduino boilerplate
python scripts/generate_config.py input.json --framework arduino --format text

# Generate ESP-IDF boilerplate
python scripts/generate_config.py input.json --framework espidf --format text
```

### Input JSON Format

Both scripts accept the same JSON structure:

```json
{
  "platform": "esp32s3",
  "module": "WROOM",
  "wifi_enabled": true,
  "pins": [
    {
      "gpio": 21,
      "function": "I2C_SDA",
      "protocol_bus": "i2c",
      "device": "BME280",
      "pull": "external_up"
    },
    {
      "gpio": 22,
      "function": "I2C_SCL",
      "protocol_bus": "i2c",
      "device": "BME280",
      "pull": "external_up"
    }
  ]
}
```

## Supported Variants

| Variant | Validation | Code Gen | Reference Docs | Best For |
|---------|:----------:|:--------:|:--------------:|----------|
| ESP32   | Yes | Yes | Yes | Bluetooth Classic, legacy projects |
| ESP32-S2 | Yes | Yes | Yes | Ultra-low power, USB OTG/HID |
| ESP32-S3 | Yes | Yes | Yes | AI/ML, complex GUIs, cameras |
| ESP32-C3 | Yes | Yes | Yes | Budget IoT nodes (RISC-V) |
| ESP32-C6 | Yes | Yes | Yes | Wi-Fi 6, Matter/Thread, Zigbee |
| ESP32-C2 | - | - | Yes | Ultra-low-cost WiFi/BLE |
| ESP32-C5 | - | - | Yes | Wi-Fi 6 dual-band |
| ESP32-H2 | - | - | Yes | Zigbee/Thread hub (no WiFi) |
| ESP32-P4 | - | - | Yes | Multimedia, H.264, dual MIPI |

## Safety Checks

The plugin actively prevents these common hardware mistakes:

| Check | What It Catches |
|-------|----------------|
| **GPIO12 Flash Voltage Trap** | Pulling GPIO12 HIGH at boot sets flash to 1.8V, potentially bricking 3.3V modules |
| **ADC2/WiFi Conflict** | ADC2 pins are unavailable when WiFi is active on ESP32/S2/S3 |
| **Flash Pin Protection** | Blocks assignment of GPIO6-11 (ESP32), GPIO12-17 (C3), GPIO24-29 (C6), GPIO26-32 (S2/S3) |
| **Input-Only Pins** | Rejects output assignments to GPIO34-39 (ESP32) or GPIO46 (S2/S3) |
| **PSRAM Conflicts** | Blocks GPIO16-17 on WROVER modules |
| **Non-Exposed Pins** | Rejects pins not physically bonded on the module (GPIO20, 24, 28-31, 37, 38 on WROOM) |
| **Current Budget** | Warns when estimated GPIO current approaches the 200mA limit |

## Reference Documentation

The plugin includes structured reference docs that Claude loads on demand:

### ESP32 Hardware
- Per-variant GPIO pin databases with usability ratings
- Strapping pin behavior and boot mode implications
- Protocol quick reference (I2C, SPI, UART, PWM, 1-Wire, ADC, DAC)
- Electrical constraints (voltage levels, current limits, pull-up requirements)

### LVGL (v8.2 - v9.5)
- Per-version API references with function signatures
- Complete widget catalogs (32+ widgets in v8, 37 in v9.5)
- v8-to-v9 migration guide with 100+ renamed functions
- ESP32 integration guide with SPI display, I2C touch, PSRAM, and FreeRTOS setup

### Waveshare
- 60+ ESP32 dev board specs with GPIO pinout tables
- LCD display modules (SPI, I2C, parallel, round, e-paper)
- Display controller ICs (ST7789, ILI9341, GC9A01, etc.)
- Touch controller ICs (CST816S, GT911, FT6336, XPT2046)

## Plugin Structure

```
ESP32-AI-Agent-Skill/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── skills/
│   └── esp32/
│       └── SKILL.md          # Main skill (auto-activates on ESP32 topics)
├── references/               # Loaded on demand by the skill
│   ├── platforms/            # GPIO databases, pin specifics
│   ├── esp32*/               # Per-variant spec sheets
│   ├── lvgl/                 # LVGL v8.2-v9.5
│   └── waveshare/            # Waveshare boards and displays
├── scripts/                  # Validation and code generation
│   ├── validate_pinmap.py
│   ├── generate_config.py
│   └── platforms/
└── tests/                    # 50 automated tests
```

## Testing

```bash
pip install pytest
python3 -m pytest tests/ -v
```

## Contributing

Contributions welcome. To extend the reference documentation:

- **New ESP32 variant**: Add `references/esp32-XX/specs.md`
- **New LVGL version**: Add `references/lvgl/vX.Y/README.md` and `api-reference.md`
- **New Waveshare board**: Add to the appropriate file in `references/waveshare/dev-boards/`
- **New display/touch controller**: Add to `references/waveshare/common/`

## Author

[ezrover](https://github.com/ezrover)

## License

MIT
