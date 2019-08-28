#!/usr/bin/env bash

sslcmd=openssl

unameOut="$(uname -s)"
case "${unameOut}" in
    MINGW*)     sslcmd="winpty openssl";;
esac

$sslcmd genrsa -des3 -out rootca.key 4096
$sslcmd req -x509 -new -nodes -key rootca.key -sha256 -days 1024 -out rootca.crt -config root.csr.cnf
$sslcmd req -new -sha256 -nodes -out server.csr -newkey rsa:4096 -keyout server.key -config server.csr.cnf
$sslcmd x509 -req -in server.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -out server.crt -days 500 -sha256 -extfile v3.ext
rm server.csr rootca.srl
