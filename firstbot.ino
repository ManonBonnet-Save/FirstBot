
//def des pins
int pin_motor_g_direction = 7;
int pin_motor_g_speed = 9;
int pin_motor_d_direction = 8;
int pin_motor_d_speed = 10;

//def des variables
char motor_g_d_direction;
char motor_g_direction;
char motor_d_direction;
boolean motor_g_speed;
boolean motor_d_speed;
char buffer[3];


void setup(){
  //mise des pins en sortie
  pinMode(pin_motor_g_direction, OUTPUT);
  pinMode(pin_motor_d_direction, OUTPUT);
  pinMode(pin_motor_g_speed, OUTPUT);
  pinMode(pin_motor_d_speed, OUTPUT);

  //on fixe le baudrate
  Serial.begin(9600);
  Serial.write('z');
}
  
  void loop(){
    //on recupere les commandes de la rasp
      Serial.readBytes(buffer,3);
      motor_g_d_direction = buffer[0];
      if(motor_g_d_direction == 1){
        motor_g_direction = LOW;
        motor_d_direction = HIGH;
      }
      else if(motor_g_d_direction == 16){
        motor_g_direction = HIGH;
        motor_d_direction = LOW;
      }
      else if(motor_g_d_direction == 17){
        motor_g_direction = HIGH;
        motor_d_direction = HIGH;
      }
      else{
        motor_g_direction = LOW;
        motor_d_direction = LOW;
      }
      digitalWrite(pin_motor_g_direction,motor_g_direction);
      digitalWrite(pin_motor_d_direction,motor_d_direction);
  
      motor_g_speed = buffer[1];
      analogWrite(pin_motor_g_speed,motor_g_speed);
  
      motor_d_speed = buffer[2];
      analogWrite(pin_motor_d_speed,motor_d_speed);
  
  }





