// Standalone ESP32-S3 multimeter test. Do not connect an RC board or motor.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "driver/gpio.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "sdkconfig.h"

#if !CONFIG_IDF_TARGET_ESP32S3
#error "Select the esp32s3 target for this bench project."
#endif

#if CONFIG_GPIO_BENCH_PIN_A == CONFIG_GPIO_BENCH_PIN_B
#error "The two standalone test GPIOs must be different."
#endif

static const gpio_num_t pin_a = CONFIG_GPIO_BENCH_PIN_A;
static const gpio_num_t pin_b = CONFIG_GPIO_BENCH_PIN_B;
static const int64_t pulse_us = INT64_C(10000000);
static QueueHandle_t command_queue;

static void outputs_low(void)
{
    ESP_ERROR_CHECK(gpio_set_level(pin_a, 0));
    ESP_ERROR_CHECK(gpio_set_level(pin_b, 0));
}

// Only this task changes outputs after initialization. Console input may block
// independently; inactivity in getchar() cannot prevent checking the deadline.
static void output_task(void *unused)
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

        // Always return both outputs LOW before selecting either test output.
        outputs_low();
        active = false;

        if (command == '1' || command == '2') {
            const gpio_num_t selected = command == '1' ? pin_a : pin_b;
            ESP_ERROR_CHECK(gpio_set_level(selected, 1));
            deadline_us = esp_timer_get_time() + pulse_us;
            active = true;
            printf("GPIO %d HIGH for about 10 seconds; other test GPIO LOW.\n",
                   (int)selected);
        } else {
            puts("Both test GPIOs LOW.");
        }
    }
}

void app_main(void)
{
    // Preload LOW before enabling the two selected output drivers.
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
    const BaseType_t task_created = xTaskCreate(output_task, "gpio_output",
                                               3072, NULL, 5, NULL);
    ESP_ERROR_CHECK(task_created == pdPASS ? ESP_OK : ESP_ERR_NO_MEM);

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("\nSTANDALONE GPIO BENCH: A=GPIO %d, B=GPIO %d\n",
           (int)pin_a, (int)pin_b);
    puts("Keep the RC board, battery, and motors disconnected from the ESP32.");
    puts("1: A HIGH briefly | 2: B HIGH briefly | 0 or s: both LOW");
    puts("No automatic HIGH sequence. Unknown commands request both LOW.");

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

        // A one-item queue keeps only the newest pending command.
        const char command = (input == '1' || input == '2') ? (char)input : '0';
        const BaseType_t queued = xQueueOverwrite(command_queue, &command);
        ESP_ERROR_CHECK(queued == pdPASS ? ESP_OK : ESP_FAIL);
    }
}
