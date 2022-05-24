/*
   --------------------------------------------------------------------------------------------------------------------
   Example sketch/program showing how to read data from a PICC to serial.
   --------------------------------------------------------------------------------------------------------------------
   This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid

   Example sketch/program showing how to read data from a PICC (that is: a RFID Tag or Card) using a MFRC522 based RFID
   Reader on the Arduino SPI interface.

   When the Arduino and the MFRC522 module are connected (see the pin layout below), load this sketch into Arduino IDE
   then verify/compile and upload it. To see the output: use Tools, Serial Monitor of the IDE (hit Ctrl+Shft+M). When
   you present a PICC (that is: a RFID Tag or Card) at reading distance of the MFRC522 Reader/PCD, the serial output
   will show the ID/UID, type and any data blocks it can read. Note: you may see "Timeout in communication" messages
   when removing the PICC from reading distance too early.

   If your reader supports it, this sketch/program will read all the PICCs presented (that is: multiple tag reading).
   So if you stack two or more PICCs on top of each other and present them to the reader, it will first output all
   details of the first and then the next PICC. Note that this may take some time as all data blocks are dumped, so
   keep the PICCs at reading distance until complete.

   @license Released into the public domain.

   Typical pin layout used:
   -----------------------------------------------------------------------------------------
               MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
               Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
   Signal      Pin          Pin           Pin       Pin        Pin              Pin
   -----------------------------------------------------------------------------------------
   RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
   SPI SS      SDA(SS)      10            53        D10        10               10
   SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
   SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
   SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
*/

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10          // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

MFRC522::MIFARE_Key key;

void setup() {

  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card

  // Prepare the key (used both as key A and as key B)
  // using FFFFFFFFFFFFh which is the default at chip delivery from the factory
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println(F("Scan a MIFARE Classic PICC to demonstrate read and write."));
  Serial.print(F("Using key (for A and B):"));
  dump_byte_array(key.keyByte, MFRC522::MF_KEY_SIZE);
  Serial.println();

  Serial.println(F("BEWARE: Data will be written to the PICC, in sector #1"));

  const char* c = "abcd";
  //  Serial.println(atoi(c));
  //  for(int i=0; i<sizeof(message); i++){
  //    Serial.println(message[i]);
  //  }

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
    return;

  // Show some details of the PICC (that is: the tag/card)
  Serial.print(F("Card UID:"));
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();
  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(piccType));

  // Check for compatibility
  if (    piccType != MFRC522::PICC_TYPE_MIFARE_MINI
          &&  piccType != MFRC522::PICC_TYPE_MIFARE_1K
          &&  piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("This sample only works with MIFARE Classic cards."));
    return;
  }

  String currency = "XMR";
  String address = "42eKczsBGi5TXjpnHEovnk9R4YbZMBT6MFqfyhiTYEUUjWBepy5vPSYhK4N1Tr79nNgZAz4aqHj47VSukPkA4nWqBt36HjW";
  Serial.println(address.length() + currency.length() + 2);
  //    write_wallet_address(currency, address, key, key);

  read_wallet_address(8, key);
}

void write_wallet_address(String currency, String address, MFRC522::MIFARE_Key keyA, MFRC522::MIFARE_Key keyB) {

  // start on sector 2
  byte first_sector = 2;
  byte first_block = 8;
  byte next_trailing = 11;
  byte block_size = 16;
  byte blocks_per_sector = 4;

  String prefix = ".";
  String deliminator = ":";
  String terminator = "!";

  // concatenate currency, address, deliminator, terminator
  String info = prefix + currency + deliminator + address + terminator;
  Serial.println(info);

  // convert address to char array
  int info_length = (info.length() / block_size);
  if ((info_length % 16) != 0) {
    info_length += 1;
  } info_length *= 16;
  char data[info_length];
  info.toCharArray(data, info_length);

  // determine how many blocks will be used
  float num_blocks = (sizeof(data) / (float)block_size);
  Serial.println(sizeof(data));
  if (num_blocks - round(num_blocks) != 0.0) {
    num_blocks = (int)num_blocks + 1;
  }

  //  Serial.println(num_blocks);

  // determine how many sectors will be used
  int num_sectors = round(num_blocks / 4);

  int _current = 0;

  // convert message into an array of individual blocks
  byte blocks[(int)num_blocks][block_size];

  for (int i = 0; i < (int)num_blocks; i++) {
    for (int j = 0; j < block_size; j++) {
      blocks[i][j] = data[_current];
      Serial.print(data[_current]); Serial.print(" ");

      // if we haven't filled a whole block, write zeroes to the rest of it
      if (data[_current] == '!' && j < block_size) {
        Serial.print("found terminator at poisition: "); Serial.println(j);
        for (int k = j + 1; k < block_size; k++) {
          blocks[i][k] = byte('!');
          Serial.print("putting terminator at "); Serial.println(k);
        }
        break;
      }

      _current++;

    }
  }

  for (int i = 0; i < (int)num_blocks; i++) {
    Serial.print("Block ");
    Serial.println(i);
    for (int j = 0; j < block_size; j++) {
      Serial.print(blocks[i][j]);
      Serial.print(" ");
    }
    Serial.println();
  }

  //  dump_byte_array(key.keyByte, MFRC522::MF_KEY_SIZE);

  MFRC522::StatusCode status;
  byte buffer[18];
  byte size = sizeof(buffer);

  // Authenticate using key A
  Serial.println(F("Authenticating using key A..."));
  status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, next_trailing, &keyA, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  //  // Show the whole sector as it currently is
  //  Serial.println(F("Current data in sector:"));
  //  mfrc522.PICC_DumpMifareClassicSectorToSerial(&(mfrc522.uid), &keyA, first_sector);
  //  Serial.println();
  //
  //  // Read data from the block
  //  Serial.print(F("Reading data from block ")); Serial.print(first_block);
  //  Serial.println(F(" ..."));
  //  status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(first_block, buffer, &size);
  //  if (status != MFRC522::STATUS_OK) {
  //    Serial.print(F("MIFARE_Read() failed: "));
  //    Serial.println(mfrc522.GetStatusCodeName(status));
  //  }
  //  Serial.print(F("Data in block ")); Serial.print(first_block); Serial.println(F(":"));
  //  dump_byte_array(buffer, 16); Serial.println();
  //  Serial.println();

  // Authenticate using key B
  Serial.println(F("Authenticating again using key B..."));
  status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_B, next_trailing, &keyB, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  // for each block to be written, starting with the first, write to the sector
  int i = 0;
  for (int blockAddr = first_block; blockAddr < (first_block + num_blocks + 1); blockAddr++) {

    // if this is the next trailing block, skip it and increment next_trailing
    // not doing so will brick the card
    if (blockAddr == next_trailing) {
      blockAddr++; next_trailing += 4;
      // authenticate this next sector using key B
      status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_B, next_trailing, &keyB, &(mfrc522.uid));
      if (status != MFRC522::STATUS_OK) {
        Serial.print(F("PCD_Authenticate() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
      }
    }

    // Write data to the block
    Serial.print(F("Writing data into block ")); Serial.println(blockAddr);
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Write(blockAddr, blocks[i], block_size);
    if (status != MFRC522::STATUS_OK) {
      Serial.print(F("MIFARE_Write() failed: "));
      Serial.println(mfrc522.GetStatusCodeName(status));
    }

    i++;

  }

  Serial.println();

  // Dump debug info about the card; PICC_HaltA() is automatically called
  mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  // Halt PICC
  mfrc522.PICC_HaltA();

  mfrc522.PCD_StopCrypto1();


}

void read_wallet_address(byte starting_block, MFRC522::MIFARE_Key keyA) {

  // start on sector 2
  byte first_sector = 2;
  byte first_block = 8; byte root_block = first_block;
  byte next_trailing = 11;
  byte block_size = 16;
  byte blocks_per_sector = 4;
  byte top_block = 63;

  char deliminator = '!';
  char terminator = '!';

  MFRC522::StatusCode status;
  byte buffer[18];
  byte size = sizeof(buffer);

  // char array of read data
  byte data[20];

  // start at the first sector
  bool terminated = false;
  int dataindex;
  while (!terminated) {

    // Authenticate using key A
    Serial.println(F("Authenticating using key A..."));
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, next_trailing, &keyA, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
      Serial.print(F("PCD_Authenticate() failed: "));
      Serial.println(mfrc522.GetStatusCodeName(status));
      return;
    }

    for (int i = root_block; i < next_trailing; i++) {
//      Serial.print("block: "); Serial.println(i);
      // Read data from the block
      //      Serial.print(F("Reading data from block ")); Serial.print(i);
      status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(i, buffer, &size);
      if (status != MFRC522::STATUS_OK) {
        //        Serial.print(F("MIFARE_Read() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
      }
//      Serial.print(F("Data in block ")); Serial.print(i); Serial.println(F(":"));
//      dump_byte_array(buffer, 16); Serial.println();
//      Serial.println();

      // dump read data into data array
      int correction_factor = ((root_block - first_block) / blocks_per_sector) * block_size;
      dataindex = 0;
      for (int j = (i - first_block) * block_size; j < (i - first_block + 1)*block_size; j++) {
//        dataindex = j - correction_factor;
        data[dataindex] = buffer[(j - ((i - first_block) * block_size))];
//        Serial.print(char(data[dataindex])); Serial.print(" -> "); Serial.print(dataindex); Serial.print(", ");
        dataindex++;
      } 
//      Serial.println();

//      Serial.println(dataindex);
      for (int i = 0; i < dataindex; i++) {
        Serial.print(char(data[i]));
            Serial.print(" ");
      }

            // if the buffer ends with the termination sequence, stop reading
      if (buffer[15] == byte(terminator)) {
        terminated = true;
        break;
      }

    }

    root_block += blocks_per_sector;
    next_trailing += blocks_per_sector;

  }

  //  // Show the whole sector as it currently is
  //  Serial.println(F("Current data in sector:"));
  //  mfrc522.PICC_DumpMifareClassicSectorToSerial(&(mfrc522.uid), &keyA, first_sector);
  //  Serial.println();
  //
  //  // Read data from the block
  //  Serial.print(F("Reading data from block ")); Serial.print(first_block);
  //  Serial.println(F(" ..."));
  //  status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(first_block, buffer, &size);
  //  if (status != MFRC522::STATUS_OK) {
  //    Serial.print(F("MIFARE_Read() failed: "));
  //    Serial.println(mfrc522.GetStatusCodeName(status));
  //  }
  //  Serial.print(F("Data in block ")); Serial.print(first_block); Serial.println(F(":"));
  //  dump_byte_array(buffer, 16); Serial.println();
  //  Serial.println();
  //
  //  for (int i = 0; i < sizeof(buffer); i++) {
  //    Serial.print(char(buffer[i]));
  //    Serial.print(" ");
  //  }

}

void loop() {

}

/**
   Helper routine to dump a byte array as hex values to Serial.
*/
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
