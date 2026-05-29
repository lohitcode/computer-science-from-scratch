CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11

.PHONY: all test clean run

all:
	$(CC) $(CFLAGS) main.c -o myprogram

test:
	$(CC) $(CFLAGS) main.c -o myprogram
	@./myprogram

run:
	@./myprogram

clean:
	rm -f myprogram
	rm -rf *.dSYM
