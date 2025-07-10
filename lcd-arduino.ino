#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>

hd44780_I2Cexp lcd; // I2C-connected LCD object

const int LCD_COLS = 20;
const int LCD_ROWS = 4;

String currentInput = "";

void setup() {
    int status = lcd.begin(LCD_COLS, LCD_ROWS);
    if (status) {
        hd44780::fatalError(status); // LED blink on init failure
    }

    Serial.begin(9600);
    lcd.clear();
    lcd.print("Waiting for song...");
}

void loop() {
    while (Serial.available()) {
        char ch = Serial.read();
        if (ch == '\n') {
            showVerse(currentInput);
            currentInput = "";
        } else {
            currentInput += ch;
        }
    }
}

void showVerse(const String& verse) {
    lcd.clear();

    // Break the string into lines of max 20 chars and print each
    for (int i = 0; i < LCD_ROWS; i++) {
        int start = i * LCD_COLS;
        if (start < verse.length()) {
            lcd.setCursor(0, i);
            lcd.print(verse.substring(start, start + LCD_COLS));
        }
    }
}
