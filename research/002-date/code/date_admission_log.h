#ifndef DATE_ADMISSION_LOG_H
#define DATE_ADMISSION_LOG_H
/* Passive diagnostic logger for libCacheSim W-TinyLFU.
 * Compile only into the instrumented translation unit.
 * Enabled with DATE_ADMISSION_LOG=/path/to/log.csv.
 */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct date_admission_logger {
  FILE *file;
  char io_buffer[64 * 1024];
  uint64_t prev_n_req;
  uint32_t ordinal;
  int io_failed;
} date_admission_logger_t;

static date_admission_logger_t *date_logger_open_from_env(void) {
  const char *path = getenv("DATE_ADMISSION_LOG");
  if (!path || !*path) return NULL;
  date_admission_logger_t *logger = (date_admission_logger_t *)calloc(1, sizeof(*logger));
  if (!logger) return NULL;
  logger->prev_n_req = UINT64_MAX;
  logger->file = fopen(path, "wb");
  if (!logger->file) { free(logger); return NULL; }
  setvbuf(logger->file, logger->io_buffer, _IOFBF, sizeof(logger->io_buffer));
  if (fprintf(logger->file, "n_req,ordinal,trigger,candidate,victim,freq_candidate,freq_victim,admit\n") < 0)
    logger->io_failed = 1;
  return logger;
}

static void date_logger_record(date_admission_logger_t *logger, uint64_t n_req,
                               uint64_t trigger, uint64_t candidate,
                               uint64_t victim, int freq_candidate,
                               int freq_victim, int admit) {
  if (!logger) return;
  if (logger->prev_n_req != n_req) {
    logger->prev_n_req = n_req;
    logger->ordinal = 0;
  }
  const uint32_t ordinal = logger->ordinal++;
  if (fprintf(logger->file,
              "%" PRIu64 ",%" PRIu32 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%d,%d,%d\n",
              n_req, ordinal, trigger, candidate, victim,
              freq_candidate, freq_victim, admit) < 0) {
    logger->io_failed = 1;
  }
}

static int date_logger_close(date_admission_logger_t *logger) {
  if (!logger) return 0;
  const int failed = logger->io_failed || fflush(logger->file) != 0;
  const int close_failed = fclose(logger->file) != 0;
  free(logger);
  return failed || close_failed;
}
#endif
