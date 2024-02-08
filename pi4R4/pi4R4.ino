// Triggerbox BNC CNC thomas.quettier2@unibo.it 2023

// Pins setting
int LedPin = 13; 
int ConditionPin = 9, TestPin = 8, BioPin = 7;

// Variables setting
int TriggerDuration = 2; // Duration between high and low (ms)
int IPI = 2, test = 4; // Inter pulse interval (ms)


void setup() {
  pinMode(LedPin, OUTPUT); // Initialize the LED pin as an output
  pinMode(ConditionPin, OUTPUT); // Initialize the BNC pin as an output
  pinMode(TestPin, OUTPUT); // Initialize the BNC pin as an output
  pinMode(BioPin, OUTPUT); // Initialize the BNC pin as an output
  Serial1.begin(115200); // Set baud rate
}

void loop() {
  digitalWrite(LedPin, HIGH); // LED high to indicate the Arduino is powered
  
  if (Serial1.available() > 0) {
    String command = Serial1.readStringUntil('\n');
    
    if (command.startsWith("SET,IPI1,")) {
      // Extract the number after "SET,IPI," and convert to integer
      IPI = command.substring(9).toInt();
      IPI = IPI - TriggerDuration;
    } 
    else if (command.startsWith("SET,test,")) {
      // Extract the number after "SET,IPI," and convert to integer
      test = command.substring(9).toInt();
      if (test == 1){
        digitalWrite(TestPin, HIGH);
        delay(TriggerDuration);
        digitalWrite(TestPin, LOW);
      }
      else if (test == 2){
        digitalWrite(ConditionPin, HIGH);
        delay(TriggerDuration);
        digitalWrite(ConditionPin, LOW);
      }
      else if (test == 3){
        digitalWrite(BioPin, HIGH);
        delay(TriggerDuration);
        digitalWrite(BioPin, LOW);
      }
    } 
    else if (command == "1") {
      digitalWrite(BioPin, HIGH);
      digitalWrite(ConditionPin, HIGH);
      delay(TriggerDuration);
      digitalWrite(ConditionPin, LOW);
      digitalWrite(BioPin, LOW);
      delay(IPI);
      digitalWrite(TestPin, HIGH);
      delay(TriggerDuration);
      digitalWrite(TestPin, LOW);
    }
  }
}
