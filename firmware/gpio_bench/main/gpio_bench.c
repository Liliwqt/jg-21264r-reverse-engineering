// GPIO meter checks, plus an opt-in manually armed M1 pulse experiment.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "driver/gpio.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "motor_bench_state.h"
#include "sdkconfig.h"

#if !CONFIG_IDF_TARGET_ESP32S3
#error "Select the esp32s3 target for this bench project."
#endif
#if CONFIG_GPIO_BENCH_PIN_A == CONFIG_GPIO_BENCH_PIN_B
#error "The two test GPIOs must be different."
#endif
#if CONFIG_GPIO_BENCH_MOTOR_TEST && \
    (CONFIG_GPIO_BENCH_PIN_A != 4 || CONFIG_GPIO_BENCH_PIN_B != 5)
#error "The documented M1 experiment requires GPIO4 and GPIO5."
#endif

static const gpio_num_t pin_a = CONFIG_GPIO_BENCH_PIN_A;
static const gpio_num_t pin_b = CONFIG_GPIO_BENCH_PIN_B;
static QueueHandle_t command_queue;

static void outputs_low(void)
{
    ESP_ERROR_CHECK(gpio_set_level(pin_a, 0));
    ESP_ERROR_CHECK(gpio_set_level(pin_b, 0));
}

#if CONFIG_GPIO_BENCH_MOTOR_TEST
typedef struct {
    motor_bench_phase_t phase;
    unsigned output;
} motor_notice_t;

static QueueHandle_t notice_queue;
static TaskHandle_t motor_output_handle;

// Console writes may block; this lower-priority task never controls GPIOs.
static void motor_notice_task(void *unused)
{
    (void)unused;
    motor_notice_t notice;
    for (;;) {
        if (xQueueReceive(notice_queue, &notice, portMAX_DELAY) != pdTRUE) {
            continue;
        }
        switch (notice.phase) {
        case MOTOR_BENCH_IDLE:
            puts("DISARMED: both LOW. Send a, wait for ARMED, then 1 or 2.");
            break;
        case MOTOR_BENCH_ARMED:
            puts("ARMED for 5 seconds: choose 1 or 2. 0 cancels.");
            break;
        case MOTOR_BENCH_PULSE:
            printf("PULSE %u: about 500 ms. 0 requests both LOW.\n", notice.output);
            break;
        case MOTOR_BENCH_COOLDOWN:
            puts("Both LOW. Cooldown 2 seconds; wait for DISARMED.");
            break;
        }
    }
}

// This task alone changes outputs after startup. It never prints or waits for
// console output. Full notice queues drop messages rather than delay LOW.
static void motor_output_task(void *unused)
{
    (void)unused;
    motor_bench_state_t state;
    motor_bench_init(&state);
    const motor_notice_t initial = {.phase = state.phase, .output = 0};
    (void)xQueueSend(notice_queue, &initial, 0);

    for (;;) {
        char command = '\0';
        (void)xQueueReceive(command_queue, &command, pdMS_TO_TICKS(20));
        // Stops use a separate notification, so a following direction/arm
        // character cannot overwrite a pending stop in the one-item queue.
        if (ulTaskNotifyTake(pdTRUE, 0) != 0) {
            (void)xQueueReset(command_queue);
            command = '0';
        }
        const motor_bench_phase_t old_phase = state.phase;
        const unsigned old_output = state.output;
        motor_bench_step(&state, esp_timer_get_time(), command);
        if (state.output != old_output) {
            outputs_low();
            if (state.output != 0) {
                const gpio_num_t selected = state.output == 1 ? pin_a : pin_b;
                ESP_ERROR_CHECK(gpio_set_level(selected, 1));
            }
        }
        if (state.phase != old_phase) {
            const motor_notice_t notice = {
                .phase = state.phase,
                .output = state.output,
            };
            (void)xQueueSend(notice_queue, &notice, 0);
        }
    }
}
#else
// Original ten-second generator: only for unloaded meter measurements.
static void standalone_output_task(void *unused)
{
    (void)unused;
    bool active = false;
    int64_t deadline_us = 0;
    for (;;) {
        if (active && esp_timer_get_time() >= deadline_us) {
            outputs_low();
            active = false;
            puts("Timeout: both test GPIOs LOW.");
        }
        char command = '0';
        if (xQueueReceive(command_queue, &command, pdMS_TO_TICKS(20)) != pdTRUE) {
            continue;
        }
        outputs_low();
        active = false;
        if (command == '1' || command == '2') {
            const gpio_num_t selected = command == '1' ? pin_a : pin_b;
            ESP_ERROR_CHECK(gpio_set_level(selected, 1));
            deadline_us = esp_timer_get_time() + INT64_C(10000000);
            active = true;
            printf("GPIO %d HIGH for about 10 seconds; other test GPIO LOW.\n",
                   (int)selected);
        } else {
            puts("Both test GPIOs LOW.");
        }
    }
}
#endif

void app_main(void)
{
    outputs_low();
    const gpio_config_t config = {
        .pin_bit_mask = (UINT64_C(1) << pin_a) | (UINT64_C(1) << pin_b),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&config));
    outputs_low();
    command_queue = xQueueCreate(1, sizeof(char));
    ESP_ERROR_CHECK(command_queue != NULL ? ESP_OK : ESP_ERR_NO_MEM);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

#if CONFIG_GPIO_BENCH_MOTOR_TEST
    printf("\nMOTOR BENCH: 500 ms | A=GPIO %d, B=GPIO %d\n",
           (int)pin_a, (int)pin_b);
    puts("M1 only, verified 1k/10k interface. All other motors disconnected.");
    puts("Keep RC battery disconnected while flashing. No Wi-Fi or PWM.");
    notice_queue = xQueueCreate(8, sizeof(motor_notice_t));
    ESP_ERROR_CHECK(notice_queue != NULL ? ESP_OK : ESP_ERR_NO_MEM);
    const BaseType_t logger_created = xTaskCreate(motor_notice_task, "bench_log",
                                                 3072, NULL, 3, NULL);
    ESP_ERROR_CHECK(logger_created == pdPASS ? ESP_OK : ESP_ERR_NO_MEM);
    const BaseType_t task_created = xTaskCreate(motor_output_task, "motor_output",
                                               3072, NULL, 5, &motor_output_handle);
#else
    printf("\nSTANDALONE GPIO BENCH: A=GPIO %d, B=GPIO %d\n",
           (int)pin_a, (int)pin_b);
    puts("Keep the RC board, battery, and motors disconnected from the ESP32.");
    puts("1: A HIGH briefly | 2: B HIGH briefly | 0 or s: both LOW");
    puts("No automatic HIGH sequence. Unknown commands request both LOW.");
    const BaseType_t task_created = xTaskCreate(standalone_output_task, "gpio_output",
                                               3072, NULL, 5, NULL);
#endif
    ESP_ERROR_CHECK(task_created == pdPASS ? ESP_OK : ESP_ERR_NO_MEM);

    for (;;) {
        const int input = getchar();
        if (input == EOF) {
            clearerr(stdin);
            vTaskDelay(pdMS_TO_TICKS(20));
            continue;
        }
        if (input == '\r' || input == '\n') {
            continue;
        }
        char command = (input == '1' || input == '2') ? (char)input : '0';
#if CONFIG_GPIO_BENCH_MOTOR_TEST
        if (input == 'a') {
            command = 'a';
        } else if (command == '0') {
            xTaskNotifyGive(motor_output_handle);
            continue;
        }
#endif
        const BaseType_t queued = xQueueOverwrite(command_queue, &command);
        ESP_ERROR_CHECK(queued == pdPASS ? ESP_OK : ESP_FAIL);
    }
}
