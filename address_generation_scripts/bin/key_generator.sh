#!/bin/bash
#echo Hello, World!

Keys=()

passphrase="Today i am about to make history and sit at the hall of fame"

#generating private key for the wallet account
private_key=$PASSPHRASE | openssl sha256

#generating public key from the private key of the wallet account
public_key=openssl ec -inform DER -text -noout -in <(cat <(echo -n "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855") <(echo -n '12345678') <(echo -n "a00706052b8104000a") | xxd -r -p) 2>/dev/null | tail -6 | head -5 | sed 's/[ :]//g' | tr -d '\n'

#keys+=(private_key)

echo $private_key

#echo ${Keys[@]}