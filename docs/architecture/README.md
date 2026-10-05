# System Architecture

This directory contains the architecture and system design documentation for VISIONFORGE.

## System Principle

VISIONFORGE follows:

**SENSE → ANALYZE → DECIDE → ACT → VERIFY**

## Main System Flow

```text
Product
   ↓
Sensor Detection
   ↓
Conveyor Positioning
   ↓
Camera Capture
   ↓
Computer Vision
   ↓
Assembly Verification
   ↓
PASS / FAIL Decision
   ↓
ESP32 Controller
   ↓
Conveyor / Reject Mechanism
   ↓
Verification
