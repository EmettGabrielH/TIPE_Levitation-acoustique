#define S11 B00100000     // Masque binaire, permettant de viser la broche D11 de l'Arduino Uno
#define S12 B01000000     //                                               D12 
#define S10 B00010000     //                                               D10 
#define S13 B11111111     //                                               D13 
float f = 40000;                             // Fréquence (en Hz)

#define periodeDuSignal (float)1/f*1000000   // Période = 1/Fréquence (en microsecondes)
#define tempo (float)periodeDuSignal/2       // Délai correspondant à la fréquence
float dephasage = 0;
#define delta (float)tempo*dephasage
void setup() {
  DDRB = DDRB | S10;             // Définit la broche D10 comme étant une "sortie"
  DDRB = DDRB | S11;
  DDRB = DDRB | S12;
  DDRD = DDRD | S13;
  
  analogWrite(2, 255);
  analogWrite(3, 255);
}

void loop() {
  PORTB = PORTB | S10;            // Met la sortie D10 à l'état haut
  PORTB = PORTB & ~S11;           // Met la sortie D11 à l'état bas
  _delay_us(delta);               // Crée une pause de temps delta
  PORTB = PORTB & ~S12;
  PORTD = PORTD | S13;
  
  
  _delay_us(tempo-0.15-delta);  
  PORTB = PORTB & ~S10;
  PORTB = PORTB | S11;
  _delay_us(delta);
  PORTB = PORTB | S12;
  PORTD = PORTD & ~S13;
  _delay_us(tempo-0.4-delta); 
  
}
