# Sputnik Climbing Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant integration that shows real-time occupancy data for Sputnik climbing centers in Spain.

## Features

- Real-time occupancy count for all Sputnik centers
- Occupancy percentage sensors
- Auto-updates every 5 minutes

## Supported Centers

- Alcobendas
- Las Rozas
- Berango
- Legazpi
- Chamberí
- Guindalera

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu → Custom repositories
3. Add this repository URL and select "Integration"
4. Search for "Sputnik Climbing" and install
5. Restart Home Assistant
6. Go to Settings → Devices & Services → Add Integration → Sputnik Climbing

### Manual

1. Copy the `custom_components/sputnik_climbing` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration → Sputnik Climbing

## Sensors

For each center, two sensors are created:

| Sensor | Description | Unit |
|--------|-------------|------|
| `sensor.sputnik_<center>_occupancy` | Current number of people | people |
| `sensor.sputnik_<center>_occupancy_percentage` | Occupancy as percentage | % |

## Example Automation

```yaml
automation:
  - alias: "Alert when Legazpi is busy"
    trigger:
      - platform: numeric_state
        entity_id: sensor.sputnik_legazpi_occupancy_percentage
        above: 70
    action:
      - service: notify.mobile_app
        data:
          message: "Sputnik Legazpi is getting busy ({{ states('sensor.sputnik_legazpi_occupancy_percentage') }}%)"
```

