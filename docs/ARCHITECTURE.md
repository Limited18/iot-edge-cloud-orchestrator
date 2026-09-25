# Architecture

Sensor Simulator → Mosquitto → Edge Server → Priority Engine → ML Decision → Edge/Cloud Processing → Firebase → Dashboard.

Priority Engine is deterministic and handles urgent events such as smoke/intrusion. The ML Decision Engine uses execution-context features to select Edge or Cloud. The four benchmark scenarios are normal workload, priority event, network degradation and resource contention.

Use measured experiment output rather than fabricated values in the paper.
