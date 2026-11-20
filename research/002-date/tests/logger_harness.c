#include "../src/date_admission_log.h"
#include <assert.h>
int main(void) {
  date_admission_logger_t *log = date_logger_open_from_env();
  assert(log != NULL);
  date_logger_record(log, 100, 9, 3, 4, 7, 2, 1);
  date_logger_record(log, 100, 9, 5, 4, 1, 2, 0);
  date_logger_record(log, 101, 10, 3, 8, 3, 3, 0);
  return date_logger_close(log);
}
