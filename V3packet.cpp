#include <bits/stdc++.h>
#include <openssl/sha.h>
#include<string.h>
#include<time.h>

using namespace std;

unsigned char * xorencrypt(unsigned char * message, unsigned char key[], int messagelen) {
    //int  messagelen = strlen((char*)message);
    int  keylen = strlen((char*)key);

    unsigned char * encrypted = (unsigned char*)malloc(messagelen+1);
    int i;
    for(i = 0; i < messagelen; i++) {
        encrypted[i] = message[i] ^ key[i % keylen];
    }
    encrypted[messagelen] = '\0';
    return encrypted;
}

/* aaaack but it's fast and const should make it shared text page. */
static const unsigned char pr2six[256] =
{
    /* ASCII table */
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 64, 64, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 64, 64, 64,
    64,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 64,
    64, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64
};

int Base64decode_len(const char *bufcoded)
{
    int nbytesdecoded;
    register const unsigned char *bufin;
    register int nprbytes;

    bufin = (const unsigned char *) bufcoded;
    while (pr2six[*(bufin++)] <= 63);

    nprbytes = (bufin - (const unsigned char *) bufcoded) - 1;
    nbytesdecoded = ((nprbytes + 3) / 4) * 3;

    return nbytesdecoded + 1;
}

int Base64decode(char *bufplain, const char *bufcoded)
{
    int nbytesdecoded;
    register const unsigned char *bufin;
    register unsigned char *bufout;
    register int nprbytes;

    bufin = (const unsigned char *) bufcoded;
    while (pr2six[*(bufin++)] <= 63);
    nprbytes = (bufin - (const unsigned char *) bufcoded) - 1;
    nbytesdecoded = ((nprbytes + 3) / 4) * 3;

    bufout = (unsigned char *) bufplain;
    bufin = (const unsigned char *) bufcoded;

    while (nprbytes > 4) {
    *(bufout++) =
        (unsigned char) (pr2six[*bufin] << 2 | pr2six[bufin[1]] >> 4);
    *(bufout++) =
        (unsigned char) (pr2six[bufin[1]] << 4 | pr2six[bufin[2]] >> 2);
    *(bufout++) =
        (unsigned char) (pr2six[bufin[2]] << 6 | pr2six[bufin[3]]);
    bufin += 4;
    nprbytes -= 4;
    }

    /* Note: (nprbytes == 1) would be an error, so just ingore that case */
    if (nprbytes > 1) {
    *(bufout++) =
        (unsigned char) (pr2six[*bufin] << 2 | pr2six[bufin[1]] >> 4);
    }
    if (nprbytes > 2) {
    *(bufout++) =
        (unsigned char) (pr2six[bufin[1]] << 4 | pr2six[bufin[2]] >> 2);
    }
    if (nprbytes > 3) {
    *(bufout++) =
        (unsigned char) (pr2six[bufin[2]] << 6 | pr2six[bufin[3]]);
    }

    *(bufout++) = '\0';
    nbytesdecoded -= (4 - nprbytes) & 3;
    return nbytesdecoded;
}

static const char basis_64[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

int Base64encode_len(int len)
{
    return ((len + 2) / 3 * 4) + 1;
}

int Base64encode(char *encoded, const char *string, int len)
{
    int i;
    char *p;

    p = encoded;
    for (i = 0; i < len - 2; i += 3) {
    *p++ = basis_64[(string[i] >> 2) & 0x3F];
    *p++ = basis_64[((string[i] & 0x3) << 4) |
                    ((int) (string[i + 1] & 0xF0) >> 4)];
    *p++ = basis_64[((string[i + 1] & 0xF) << 2) |
                    ((int) (string[i + 2] & 0xC0) >> 6)];
    *p++ = basis_64[string[i + 2] & 0x3F];
    }
    if (i < len) {
    *p++ = basis_64[(string[i] >> 2) & 0x3F];
    if (i == (len - 1)) {
        *p++ = basis_64[((string[i] & 0x3) << 4)];
        *p++ = '=';
    }
    else {
        *p++ = basis_64[((string[i] & 0x3) << 4) |
                        ((int) (string[i + 1] & 0xF0) >> 4)];
        *p++ = basis_64[((string[i + 1] & 0xF) << 2)];
    }
    *p++ = '=';
    }

    *p++ = '\0';
    return p - encoded;
}

void create_auth_packet3()
{   //40 byte, signature
    //1 byte , encrypt_key_number
   //2 byte, signature_kength
   //8 byte, time stamp
   //33 byte , enocded_token
   //2 byte , auth_pac_length
   //1 byte,  respond
   // 2 byte, encoded_token_length
   //13 or 14 byte, payload
   // 2 byte , payload_length
    unsigned short encodedTokenLen;
    const unsigned short tokenLen=24;
    const unsigned short signatureLen=40;
    int SHA_RESULT_LENGTH=40;
    char* Token;
    unsigned char app_id[]= "com.sanity.test";
//    unsigned char skey0[] = "SM62KphYVQN1Y1OI";
//    unsigned char skey1[] = "O2bxWuezJ5JhrdeZ";
    unsigned char *skeys[] = {
    (unsigned char *)"SM62KphYVQN1Y1OI", // sKey0 - used in auth v3 auth packet signature
    (unsigned char *)"O2bxWuezJ5JhrdeZ", // sKey1 - used for auth v3 payload encryption
    (unsigned char *)"Yab4V6u8pzM3h9u8",
    (unsigned char *)"mvLDu0c0tKw8fEd5",
    (unsigned char *)"K6Ja3ZsVF2WvBWsA",
    (unsigned char *)"7NPs6Q4xXddwUVVV",
    (unsigned char *)"HmbJ6zGm5qddMiie",
    (unsigned char *)"sMyypdfUnXaPUS3g",
    (unsigned char *)"IrrsXwfr4CCD9MuQ",
    (unsigned char *)"rzQ3HlVbtNVIQSrv"  // sKey9 - used for auth v3 payload encryption
    };

    int encrypt_key_number = 5;
    Token=(char*)malloc(1+tokenLen);
    memcpy(Token,"5b0fe4cd15b9610844933988",24);
    encodedTokenLen= Base64encode_len(24);  // Encoding in Base64
    //cout<<"Encoded TokenLen: ";
    //cout<<encodedTokenLen<<endl;
    int bodyLen=0,pos=0;
    char buffer[200]; //Payload
    int written_len = 0; //Byte count written in payload
    written_len = sprintf(buffer, "{\"isFg\" : \"%s\",\"userId\" : \"%s\",\"dUid\" : \"%s\",\"dMk\" : \"%s\",\"dMl\" : \"%s\",\"mccMnc\" : \"%s\"}","true","testUser:79eec5bdfe7c6f03","79eec5bdfe7c6f03","HMD Global","TA-1021","405-53" );
    
    buffer[written_len]='\0';
    written_len = (int)strlen(buffer);
    //cout<<"sizeof(signatureLen): "<<sizeof(signatureLen)<<endl;
    bodyLen = sizeof(encodedTokenLen) +encodedTokenLen +sizeof(signatureLen) +8+40+1+written_len+2; 
    //cout<<"BodyLen: ";
    //cout<<bodyLen<<endl;
    unsigned char* buf; //Authpac buffer
    unsigned char*req_buf;
   
    req_buf=(unsigned char*)malloc(1024+4);
    buf=(unsigned char*)malloc(1024+4);
    int respond=1;   // Response type either 1 or 0 
    
    int pos_req = 0;
    req_buf[pos_req] =(10 << 4) + 3;   //packet type
    pos_req++;
    req_buf[pos_req] = encrypt_key_number ;
    pos_req++;
    
    pos=0;
    unsigned char low, high;
    //adding body lenght in two byte
    /*low = (unsigned char) (bodyLen & 0x00ff);
    high = (unsigned char) ((bodyLen & 0xff00) >> 8);
    buf[pos] =high;
    buf[pos + 1] = low;
    pos += 2;
*/
    //Adding response in one byte
    low=(unsigned char) (respond & 0x00ff);
    buf[pos]=low;
    cout<<endl<<"First low: ";
    printf("%u\n ",low);
    pos++;
    //adding encodedTokenLen in two byte
    low = (unsigned char) (encodedTokenLen & 0x00ff);
    high = (unsigned char) ((encodedTokenLen & 0xff00) >> 8);
    buf[pos] = high;
    buf[pos + 1] = low;
    pos += 2;

    cout<<"Buf before adding token : ";
    for(int i=0;i<pos;++i)
        printf("%u ",buf[i]);
    cout<<endl;
    //Adding Encoded Token
    char  * encodedToken = (char *)malloc(sizeof(char) * (encodedTokenLen));
    short length = Base64encode(encodedToken, Token,tokenLen);
    cout<<"Encoded Token: ";
    cout<<encodedToken<<endl;
    cout<<strlen(encodedToken)<<endl;
    memcpy(buf + pos, encodedToken,encodedTokenLen);
    pos +=encodedTokenLen;

    cout<<"Buf before adding timestamp : ";
    for(int i=0;i<=pos;++i)
        printf("%u ",buf[i]);
    cout<<endl;
    //Adding current time_stamp
    //long long tym = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    long long tym = 1528200938;
    unsigned char *p = (unsigned char*)&tym;
    buf[pos+7]=p[0];
    buf[pos+6]=p[1];
    buf[pos+5]=p[2];
    buf[pos+4]=p[3];
    buf[pos+3]=p[4];
    buf[pos+2]=p[5];
    buf[pos+1]=p[6];
    buf[pos]=p[7];
    pos+=8;

    cout<<"Buf after adding timestamp : ";
    for(int i=0;i<=pos;++i)
        printf("%u ",buf[i]);
    cout<<endl;
    cout<<"TimeStamp : "<<tym<<endl;
    for(int i=7;i>=0;--i)
        printf("%u ",p[i]);
    cout<<endl;
    //Adding Signature len
    low = (unsigned char) (signatureLen & 0x00ff);
    high = (unsigned char) ((signatureLen & 0xff00) >> 8);
    buf[pos] = high;
    buf[pos + 1] = low;
    pos += 2;
    char ts_str[20];
    snprintf(ts_str,sizeof(ts_str),"%lld",tym);
    
    char buf2[256] = "";
    unsigned char digest[SHA_DIGEST_LENGTH];
    //Making signature : Using Token + tstamp + app_id
    //snprintf( buf2, sizeof(buf2), "%.*s%s%s%s",tokenLen, Token,ts_str,app_id,skeys[0]);
    snprintf(buf2, sizeof(buf2), "5b0fe4cd15b96108449339885b16311ecom.sanity.testSM62KphYVQN1Y1OI");
    cout<<buf2<<endl;
    //Encrypting using sha1
    SHA_CTX sha;
    SHA1_Init(&sha);
    SHA1_Update(&sha, (const unsigned char *)buf2, (unsigned int)strlen(buf2));
    SHA1_Final(digest, &sha);
    //cout<<digest<<endl;
    int i;
    cout<<"Digest: "<<digest;
    char result[SHA_RESULT_LENGTH+1];
    
        memset(result, 0, (SHA_RESULT_LENGTH+1)*sizeof(char));
        for(i = 0; i < 5 ; i++) {
            sprintf(&result[i*8], "%08x ", (unsigned int)digest[i]); //printf("%08x ", (unsigned int)digest[i]);
    }
    cout<<endl;
    cout<<result<<endl;
    cout<<"Buf : ";
    //Putting digest key in buffer
    memcpy(buf+pos , result, SHA_RESULT_LENGTH);
    pos+=(SHA_RESULT_LENGTH);
    for(int i=0;i<=pos;++i)
        printf("%u ",buf[i]);
    cout<<endl<<"SHA1 length: "<<SHA_RESULT_LENGTH<<endl;
    
    //Adding payload length
    low = (unsigned char) (strlen(buffer) & 0x00ff);
    high = (unsigned char) ((strlen(buffer) & 0xff00) >> 8);
    buf[pos] = high;
    buf[pos + 1] = low;
    pos += 2;
    //printf("json len %02x %02x \n",high, low);
    //Adding json payload
    memcpy(buf+pos , buffer, strlen(buffer)); 
   
    pos+= strlen(buffer);
    int x;
    buf[pos]='\0';
    cout<<endl;
    
 /* cout<<"original payload"<<endl;
    for(int i = 0 ;i<pos ;i++)
       printf("%02x ",buf[i])encrypted;
    
    cout<<endl;  
    cout<<endl;
    cout<<endl; 
  */  
    cout<<"This is buf : \n";
    unsigned char * encrypted = xorencrypt(buf, (unsigned char *)skeys[encrypt_key_number],pos);
    for(int i=0;i<=pos;++i)
        printf("%u ", buf[i]);
    cout<<endl;
    cout<<"This is encrypted buf: \n";
    for(int i=0;i<=pos;++i)
    {
        printf("%u ", encrypted[i]);
    }
    cout<<endl;
   /*
   cout<<"encrypted payload"<<endl; 
    for(int i = 0 ;i<pos ;i++)
        printf("%02x ",encrypted[i]);
    
    cout<<endl;
    cout<<endl;
    cout<<endl;
   */
    unsigned char * encrypted1 = xorencrypt(encrypted, (unsigned char *)skeys[encrypt_key_number],pos);
    
  /* unsigned char key5[]="sMyypdfUnXaPUS3g";
   unsigned char temp[]="2PzMDCumv{[`~@\F`UJP@07%T=WkxGCFnO^Atqs";
     unsigned char * encrypted2 = xorencrypt(temp, key5,strlen((char*)temp));    
    cout<<"decrypted payload temp"<<strlen((char*)temp)<<endl; 
    for(int i = 0 ;i<strlen((char*)temp) ;i++)
    printf("%02x ",encrypted2[i]);
   */
   /*
    cout<<endl;
    cout<<endl;
    cout<<endl;  
    
    cout<<"decrypted payload"<<endl;
    for(int i = 0 ;i<pos;i++)
    printf("%02x ",encrypted1[i]);
  */
    low = (unsigned char) (pos & 0x00ff);
    high = (unsigned char) ((pos & 0xff00) >> 8);
    printf("High %u\nLow %u\n",high,low );
    req_buf[pos_req] = high;
    req_buf[pos_req + 1] = low;
    pos_req += 2;
    cout<<"This is req_buf"<<endl;
    for(int i=0;i<pos_req;++i)
        printf("%02x ",req_buf[i]);
    
    memcpy(req_buf+pos_req ,encrypted , pos); 
    pos_req+=pos;
    req_buf[pos_req]='\0';

    cout<<endl;
   

    for(int i=0;i<=pos_req;++i)
        printf("%u ",req_buf[i]);
    printf("\n %d \n", pos_req);

    for(int i=0;i<=pos_req;++i)
        printf("%02x ",req_buf[i]);
    printf("\n %d \n", pos_req);
    
    return;
}

int main(void) {
    
	create_auth_packet3();

}

