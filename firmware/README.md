# Firmware implementation boundary

Firmware is not implemented yet. Arduino versus ESP-IDF remains undecided.

Before implementation, establish the physical driver pins, electrical input ownership, compatible logic levels, verified stop state, motor/socket mapping, and supported PWM behavior. See [architecture](../docs/architecture.md) and the [verification plan](../docs/verification-plan.md).

Future firmware should separate transport, command ownership/timeouts, motion logic, the measured JG-21264R adapter, and platform GPIO/PWM. No example pin assignments or runnable motor-control defaults are provided while the hardware interface is unknown.
