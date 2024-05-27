import os
import sys

com = int(input())

if com:
    os.system("g++ -std=c++17 -o gen gen.cpp" )
    os.system("g++ -std=c++17 -o correct tester.cpp")
    code = os.system("g++ -std=c++17 -o wrong cf.cpp")
    if code != 0:
        print("Compilation Error")
        exit(0)

os.system("@echo off")

for i in range(100):
    os.system("gen > input.txt")
    os.system("correct < input.txt > true.txt")
    os.system("wrong < input.txt > false.txt")
    if os.system("fc true.txt false.txt"):
        print("Wrong Answer")
        exit(0) 

print("All tests are passed")
    