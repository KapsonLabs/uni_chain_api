#!/bin/zsh
debug=$1
base58=(1 2 3 4 5 6 7 8 9 A B C D E F G H J K L M N P Q R S T U V W X Y Z a b c d e f g h i j k m n o p q r s t u v w x y z)

capitalizeHex() {
    tr "[a-f]" "[A-F]"
}

#base 58 to encode the keys to produce compressed keys
encodeBase58() {                                  
    initialones=$(sed -e 's/\(\(00\)*\).*/\1/' -e 's/00/1/g' <<<$1)
    echo -n $initialones
    bc <<<"ibase=16; n=$1; while(n>0) { n%3A ; n/=3A }" |
    tail -r |
    while read n
        do echo -n ${base58[n+1]}
    done
}

checksum() {
    xxd -p -r <<<"$1" |
    openssl dgst -sha256 -binary |
    openssl dgst -sha256 -binary |
    xxd -p -c 80 |
    head -c 8 |
    capitalizeHex
}

hexToAddress() {
    echo "$(encodeBase58 "$2$1$(checksum "$2$1")")"
}

privatekey=$(openssl ecparam -genkey -name secp256k1 -noout)
openssldescription=$(openssl ec -text <<<$privatekey 2>/dev/null)
privatekeyhex=$(head -5 <<<$openssldescription | tail -3 | fmt -120 | sed -e 's/[: ]//g' -e 's/^00//' | awk '{printf "%064s\n", $0}' | capitalizeHex)
publickeyhashhex=$(openssl ec -pubout -outform DER <<<$privatekey 2>/dev/null | tail -c 65 | openssl dgst -sha256 -binary | openssl dgst -rmd160 -binary | xxd -p -c 80 | capitalizeHex)
address=$(hexToAddress $publickeyhashhex "00")
privatekeywif=$(hexToAddress $privatekeyhex "80")

#trying to convert hex key to pem for signing transactions

(( $debug )) && echo $openssldescription > privatekey.pem
echo "Private_Key_Hex:" $privatekeyhex
echo "Private_Key_WIF:" $privatekeywif
(( $debug )) && echo "Public_Key_Hash:" $publickeyhashhex
echo "Address:" $address