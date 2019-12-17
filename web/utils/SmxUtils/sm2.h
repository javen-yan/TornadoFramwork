#ifndef _SM2_H
#define _SM2_H

#include <sm/sm2.h>

int create_key_pair(char **pub_key, char **private_key);

int icity_sm2_encrypt(char *pub_key, char *msg, int msg_length, char **ciphertext);

int icity_sm2_decrypt(char *private_key, char *ciphertext, char **clear_text, int *clear_text_length);

int icity_sm2_sign(char *private_key, char *msg, int msg_length, char **sign_text);

int icity_sm2_verify(char *pub_key, char *msg, int msg_length, char *sign_text);

#endif
