#include "motor_bench_state.h"

void motor_bench_init(motor_bench_state_t *state)
{
    *state = (motor_bench_state_t){.phase = MOTOR_BENCH_IDLE};
}

void motor_bench_step(motor_bench_state_t *state, int64_t now_us, char command)
{
    /* Expiration wins over a command arriving on the same step. A late tick
       starts the full cooldown at the actual return-to-LOW time. */
    if (state->phase == MOTOR_BENCH_PULSE && now_us >= state->deadline_us) {
        state->output = 0;
        state->phase = MOTOR_BENCH_COOLDOWN;
        state->deadline_us = now_us + MOTOR_BENCH_COOLDOWN_US;
    } else if ((state->phase == MOTOR_BENCH_ARMED ||
                state->phase == MOTOR_BENCH_COOLDOWN) &&
               now_us >= state->deadline_us) {
        state->phase = MOTOR_BENCH_IDLE;
        state->deadline_us = 0;
    }

    if (command == '\0') {
        return;
    }
    if (command == 'a') {
        if (state->phase == MOTOR_BENCH_IDLE) {
            state->phase = MOTOR_BENCH_ARMED;
            state->deadline_us = now_us + MOTOR_BENCH_ARM_US;
        }
        return;
    }
    if (command == '1' || command == '2') {
        if (state->phase == MOTOR_BENCH_ARMED) {
            state->output = command == '1' ? 1U : 2U;
            state->phase = MOTOR_BENCH_PULSE;
            state->deadline_us = now_us + MOTOR_BENCH_PULSE_US;
        }
        return;
    }

    /* Stop/unknown commands cancel arming or end a pulse. Repeated stop
       commands cannot erase an existing cooldown. */
    if (state->phase == MOTOR_BENCH_PULSE) {
        state->phase = MOTOR_BENCH_COOLDOWN;
        state->deadline_us = now_us + MOTOR_BENCH_COOLDOWN_US;
    } else if (state->phase == MOTOR_BENCH_ARMED) {
        state->phase = MOTOR_BENCH_IDLE;
        state->deadline_us = 0;
    }
    state->output = 0;
}
