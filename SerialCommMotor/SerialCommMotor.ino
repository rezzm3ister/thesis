#define echoPinF 2
#define trigPinF 3 
#define echoPinL 4 
#define trigPinL 5 
#define echoPinR 6 
#define trigPinR 7 

int i;
int run1 = 9;  // 0 to 255, 255 = max, 0 = stop
int run2 = 10; // 0 to 255, 255 = max, 0 = stop
int dir1 = 8; 
int dir2 = 11;
int command,tc;
int speed;
int manual;
int Mf,Mr;
int receivedChar;
boolean newData = false;



// defines variables
double disforward; // variable for the distance of the forward sensor
double disleft; // distance of the left sensor
double disright;// distance of the right sensor

void setup() {
  pinMode(trigPinF, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinF, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPinL, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinL, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPinR, OUTPUT); // Sets the trigPin as an       
  pinMode(echoPinR, INPUT); // Sets the echoPin as an INPUT
  
  pinMode(A0,INPUT); //manual override
  pinMode(A5,INPUT); //f/b 
  pinMode(A4,INPUT); //l/r 
  
  Serial.begin(115200);        
  for(i=8; i <=11;i=i+1) 
  {
    pinMode(i, OUTPUT);  //motor control
  }  
  delay(10);
 //stop motors 
  for(i=8; i <=11;i=i+1)
    {  
      digitalWrite(i,LOW);
    }

   Serial.println("Type Command");
  
}

void loop() { 
  
  
  //main routine here
  //disforward = measureDistance(trigPinF, echoPinF);
    //Serial.println(disforward);
    ///Serial.flush();
    //Serial.read();
    
    //recvOneChar();
 disforward = measureDistance(trigPinF, echoPinF);
 //disright = measureDistance(trigPinR, echoPinR);
 //disleft = measureDistance(trigPinL, echoPinL);
 manual = digitalRead(A0);
 Mf=analogRead(A5);
 Mr=analogRead(A4);
 //Serial.println("Forward Sensor: ");
 //Serial.println(disforward);
 //Serial.println("Right Sensor: ");
 //Serial.print(disright);
 //Serial.println("Left Sensor: ");
 //Serial.print(disleft);
  //motorcontrol154(int speed1, int mydir1, int speed2, int mydir2 ) 
  
  if (manual==1){//manual override
	  if(Mf>=900){
		  command=210;
	  }
	  else if(Mf<=100){
		  command=211;
	  }
	  else{
		  if(Mr>=900){
			  command=212;
		  }
		  else if(Mr<=100){
			  command=213;
		  }
		  else{command=214;}
	  }
  }
  else {
    if (Serial.available()) { //replace the data type from string to char/int so it can use a switch case much more cleaner code than elif spamming
    //recvOneChar(); //REMEMBER MOTOR1 IS REVERSED FOR SOME REASON
      tc = Serial.read();
      if(tc>200){
        
        if(tc==201){
          tc=Serial.read();
          if(tc<200){speed=tc;}
        }
        else{
          command=tc;
        }
      
      }
      
      //more functions can be added here
      
    }
    else{//command=200;
    }
  }

  if(disforward<20){command=211;}
  else{}
  
  //sub-200: speed
  //200 series: identifiers
  //210 series: motion
  switch (command) {
      case 210://Forward
        motorcontrol(speed,0,speed,1);
        break;
      case 211://Backward
        motorcontrol(96,1,96,0);
        break;
        case 212://Right
        motorcontrol(96,0,96,0);
        break;
        case 213://Left
        motorcontrol(96,1,96,1);
        break;
        case 214://Stop
        motorcontrol(0,0,0,0);
        break;
      default:
        motorcontrol(0,0,0,0);
        break;
    /*
        case 100://Forward
          motorcontrol(96,1,96,0);
          break;
        case 101://Backward
          motorcontrol(96,1,96,0);
          break;
         case 151://Right
          motorcontrol(96,0,96,0);
          break;
         case 150://Left
          motorcontrol(96,1,96,1);
          break;
         case 200://Stop
          motorcontrol(0,0,0,0);
          break;
        default:
          motorcontrol(0,0,0,0);
          break;
      */
      }
    /*if (command == 150){ //LEFT
      motorcontrol(154,1,154,1);
      //delay(1000);
      //motorcontrol(0,0,0,0);
    }
    else if (command == 101){ //BACKWARD 
      motorcontrol(154,1,154,0);
      //delay(750);
      //motorcontrol(0,0,0,0);
      
    }
    else if (command == 100){ //FORWARD
      motorcontrol(154,0,154,1);
      //delay(1000);
      //motorcontrol(0,0,0,0);
    }
    else if (command == 151){ //RIGHT
      motorcontrol(154,0,154,0);
      //delay(1000);
      //motorcontrol(0,0,0,0);
      //disright = measureDistance(trigPinR, echoPinR);
      //Serial.print(disright);
    }
    else if (command == 200){ //STAHP
      motorcontrol(0,0,0,0);
      //delay(1000);
      //motorcontrol(0,0,0,0);
    }
    Serial.print("Command: ");
    //showNewData(); 
  }
  else{
    motorcontrol(0,0,0,0);
  }*/
  delay(10);
} 

 
void motorcontrol(int speed1, int mydir1, int speed2, int mydir2 )  {
  // motor1
  digitalWrite(dir1,mydir1); //direction control of motor1, 1 = REVERSE
  analogWrite(run1,speed1);  //speed control of motor1, 0 =stop, 255 =fastest
  // motor2
  digitalWrite(dir2,mydir2); //direction control of motor2, 1 = forward
  analogWrite(run2,speed2);  //speed control of motor2, 0 =stop, 255 =fastest
}

long measureDistance(int trigger, int echo){
  long duration = 0;
  // Clears the trigPin condition
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echo, HIGH);
  // Calculating the distance
 return duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back) 
}
