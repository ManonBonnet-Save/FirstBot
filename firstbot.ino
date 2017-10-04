
//def des pins
int pin_motor_g_direction = 7;
int pin_motor_g_speed = 9;
int pin_motor_d_direction = 8;
int pin_motor_d_speed = 10;

//def des variables
byte motor_g_d_direction;
byte motor_g_direction;
byte motor_d_direction;
boolean motor_g_speed;
boolean motor_d_speed;


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
  if(Serial.available() > 0) {
    motor_g_d_direction = Serial.read();
    if(motor_g_d_direction == '00000001'){
      motor_g_direction = LOW;
      motor_d_direction = HIGH;
    }
    else if(motor_g_d_direction == '00010000'){
      motor_g_direction = HIGH;
      motor_d_direction = LOW;
    }
    else if(motor_g_d_direction == '00010001'){
      motor_g_direction = HIGH;
      motor_d_direction = HIGH;
    }
    else{
      motor_g_direction = LOW;
      motor_d_direction = LOW;
    }

  }

  if(Serial.available() > 0) {
    motor_g_speed = Serial.read();
  }

  if(Serial.available() > 0) {
    motor_d_speed = Serial.read();
  }
  
  //on renvoie les commandes pour control vers la rasp
  Serial.print("motor_g_d_direction=");
  Serial.println(motor_g_d_direction,DEC);
  Serial.print("motor_g_speed=");
  Serial.println(motor_g_speed,DEC);
  Serial.print("motor_d_speed=");
  Serial.println(motor_d_speed,DEC);
  
  //on affecte les commandes
  digitalWrite(pin_motor_g_direction,motor_g_direction);
  digitalWrite(pin_motor_d_direction,motor_d_direction);
  analogWrite(pin_motor_g_speed,motor_g_speed);
  analogWrite(pin_motor_d_speed,motor_d_speed);

}





