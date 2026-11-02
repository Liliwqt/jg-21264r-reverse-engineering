#ifndef MOTOR_BENCH_STATE_H
#define MOTOR_BENCH_STATE_H

#include <stdint.h>

#define MOTOR_BENCH_PULSE_US INT64_C(500000)
#define MOTOR_BENCH_ARM_US INT64_C(5000000)
#define MOTOR_BENCH_COOLDOWN_US INT64_C(2000000)

typedef enum {
    MOTOR_BENCH_IDLE,
    MOTOR_BENCH_ARMED,
    MOTOR_BENCH_PULSE,
    MOTOR_BENCH_COOLDOWN,
} motor_bench_phase_t;

typedef struct {
    motor_bench_phase_t phase;
    unsigned output; /* 0: both LOW, 1: A HIGH, 2: B HIGH */
    int64_t deadline_us;
} motor_bench_state_t;

void motor_bench_init(motor_bench_state_t *state);
/* Call regularly with monotonic microseconds; '\0' means no new command. */
void motor_bench_step(motor_bench_state_t *state, int64_t now_us, char command);

#endif
