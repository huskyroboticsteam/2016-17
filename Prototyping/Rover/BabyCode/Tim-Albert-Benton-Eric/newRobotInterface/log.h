#ifndef LOG_H
#define LOG_H

// Comment this line to disable logging. Uncomment it to enable it.
#define DEBUG

#define do_it(a) do { a; } while (0)

// Call initLogging() in setup().
#ifdef DEBUG
  #define initLogging() do_it(Serial.begin(9600))
  #define debug(x) do_it(Serial.print(x))
  #define debugln(x) do_it(Serial.println(x))
  #define debugValue(x) do_it(debug(#x "="); debug(x); debug(" ");)
  #define debuglnValue(x) do_it(debug(#x "="); debugln(x);)
#else
  #define initLogging() do_it()
  #define debug(x) do_it()
  #define debugln(x) do_it()
  #define debugValue(x) do_it()
  #define debuglnValue(x) do_it()
#endif

#endif
