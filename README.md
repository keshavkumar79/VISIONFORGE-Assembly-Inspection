# VISIONFORGE
## Vision-Based Automated Assembly Verification and Quality Inspection System

> An automated manufacturing inspection system that combines Computer Vision, Embedded Control, Sensors, Conveyor Automation, and Feedback to detect assembly defects and automatically reject defective products.

---

## 👥 Team

| Member | Role |
|---|---|
| Keshav | Computer Vision & System Integration |
| Rohit | Mechanical & Conveyor Design |
| Lakshit | Embedded & Motor Control |
| Sneha | Sensors & Automation Logic |
| Divya | Testing, Data & Documentation |

---

# 🎯 Problem Statement

In manufacturing industries, products may contain:

- Missing components
- Incorrectly positioned components
- Incorrectly oriented components
- Improper assembly

Manual inspection is repetitive, time-consuming and prone to human error.

VISIONFORGE aims to automate this inspection process using computer vision and industrial automation.

---

# 💡 Proposed Solution

The system captures an image of an assembled product using a camera and analyzes it using computer vision.

The system determines:

1. Whether all required components are present.
2. Whether components are positioned correctly.
3. Whether components have the correct orientation.
4. Whether the assembly satisfies predefined quality conditions.

The final decision is:

**PASS → Product continues**

**FAIL → Product is automatically rejected**

---

# ⚙️ System Workflow

```text
Product
   ↓
Conveyor
   ↓
Sensor Detection
   ↓
Camera Capture
   ↓
Image Processing
   ↓
Component Detection
   ↓
Position & Orientation Check
   ↓
PASS / FAIL Decision
   ↓
ESP32 / Controller
   ↓
Reject Mechanism
   ↓
Final Verification
