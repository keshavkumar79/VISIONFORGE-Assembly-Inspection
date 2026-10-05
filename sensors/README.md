# Sensors & Automation

This module contains sensor integration and automation sequencing for the VISIONFORGE system.

## Responsibilities

- IR/proximity sensor integration
- Product detection
- Conveyor positioning
- Start/stop triggering
- Inspection timing
- Automation state machine
- Sensor debouncing
- Rejection verification
- Synchronization between sensors, camera and controller

## Basic Sequence

```text
Product Detected
       ↓
Stop / Position Product
       ↓
Trigger Camera
       ↓
Wait for PASS/FAIL
       ↓
Restart Conveyor / Reject Product
       ↓
Verify Action
