#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>

hd44780_I2Cexp lcd; // auto-locating I2C LCD

// LCD size
const int LCD_COLS = 20;
const int LCD_ROWS = 4;

// Line buffer for rolling text
String lines[LCD_ROWS];
String currentInput = "";

void setup() {
    int status = lcd.begin(LCD_COLS, LCD_ROWS);
    if (status) {
        hd44780::fatalError(status); // LED blink on failure
    }

    Serial.begin(9600);
    lcd.clear();
    lcd.print("Waiting for input...");
}

void loop() {
    // Read characters from Serial
    while (Serial.available()) {
        char ch = Serial.read();
        if (ch == '\n') {
            addLine(currentInput);
            currentInput = "";
        } else {
            currentInput += ch;
        }
    }
}

// Adds a line to the buffer and scrolls display
void addLine(const String& newLine) {
    // Scroll lines up
    for (int i = 0; i < LCD_ROWS - 1; i++) {
        lines[i] = lines[i + 1];
    }

    // Add new line to bottom
    lines[LCD_ROWS - 1] = newLine.length() > LCD_COLS ? newLine.substring(0, LCD_COLS) : newLine;

    // Refresh LCD
    lcd.clear();
    for (int i = 0; i < LCD_ROWS; i++) {
        lcd.setCursor(0, i);
        lcd.print(lines[i]);
    }
}
