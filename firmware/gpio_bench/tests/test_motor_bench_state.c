#include <assert.h>
#include <stdio.h>

#include "motor_bench_state.h"

int main(void)
{
    motor_bench_state_t s;
    motor_bench_init(&s);
    assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);

    /* A held direction key cannot arm or start the motor. */
    for (int i = 0; i < 100; ++i) {
        motor_bench_step(&s, i * INT64_C(1000), i % 2 ? '1' : '2');
        assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);
    }

    /* Arming has a fixed expiration, including at the exact deadline. */
    motor_bench_step(&s, 100000, 'a');
    assert(s.phase == MOTOR_BENCH_ARMED && s.output == 0);
    motor_bench_step(&s, 200000, 'a');
    assert(s.deadline_us == 5100000);
    motor_bench_step(&s, 5100000, '1');
    assert(s.phase == MOTOR_BENCH_IDLE && s.output == 0);

    motor_bench_step(&s, 6000000, 'a');
    motor_bench_step(&s, 6100000, '1');
    assert(s.output == 1 && s.phase == MOTOR_BENCH_PULSE);
    assert(s.deadline_us == 6600000);
    /* Repeat, reverse, and arm keys cannot prolong or change an active pulse. */
    motor_bench_step(&s, 6200000, '1');
    motor_bench_step(&s, 6300000, '2');
    motor_bench_step(&s, 6400000, 'a');
    assert(s.output == 1 && s.deadline_us == 6600000);
    motor_bench_step(&s, 6599999, '\0');
    assert(s.output == 1);
    motor_bench_step(&s, 6600000, '2');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_COOLDOWN);

    motor_bench_step(&s, 6700000, 'a');
    motor_bench_step(&s, 6800000, '1');
    motor_bench_step(&s, 6900000, '0');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_COOLDOWN);
    assert(s.deadline_us == 8600000);
    motor_bench_step(&s, 8600000, '2');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);

    /* A new arm permits the other output; stop interrupts it early. */
    motor_bench_step(&s, 8700000, 'a');
    motor_bench_step(&s, 8800000, '2');
    assert(s.output == 2);
    motor_bench_step(&s, 8810000, '0');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_COOLDOWN);
    assert(s.deadline_us == 10810000);

    /* A delayed controller tick stops first and preserves a full cooldown. */
    motor_bench_step(&s, 11000000, 'a');
    motor_bench_step(&s, 11100000, '1');
    motor_bench_step(&s, 20000000, 'a');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_COOLDOWN);
    assert(s.deadline_us == 22000000);
    motor_bench_step(&s, 22000000, '1');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);

    /* Unknown commands disarm, stop an active pulse, and cannot arm. */
    motor_bench_step(&s, 23000000, 'a');
    motor_bench_step(&s, 23100000, 'x');
    motor_bench_step(&s, 23200000, '1');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);
    motor_bench_step(&s, 24000000, 'a');
    motor_bench_step(&s, 24100000, '2');
    motor_bench_step(&s, 24200000, 'x');
    assert(s.output == 0 && s.phase == MOTOR_BENCH_COOLDOWN);

    motor_bench_init(&s);
    assert(s.output == 0 && s.phase == MOTOR_BENCH_IDLE);
    puts("PASS: startup, no unarmed motion, arm expiry, fixed pulse deadline, "
         "no pulse extension/reversal, cooldown, rearming, early stop, "
         "late tick, unknown command, and reset.");
    return 0;
}
